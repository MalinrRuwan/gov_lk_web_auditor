import socket
import ssl

from cryptography import x509

from ..models.TlsObservation import TlsObservation
from ..time.SriLankaTime import SriLankaTime


class TlsInspector:
    def inspect(self, host: str, port: int = 443) -> TlsObservation:
        try:
            der = self._certificate(host, port)
            certificate = x509.load_der_x509_certificate(der)
            expires = certificate.not_valid_after_utc
            hostname_valid = self._matches(host, certificate)
            return self._observation(host, expires, hostname_valid)
        except (OSError, ssl.SSLError, ValueError) as error:
            return TlsObservation(host, "error", None, None, str(error))

    def _observation(self, host, expires, hostname_valid) -> TlsObservation:
        local_expiry = SriLankaTime.iso(expires)
        if expires <= SriLankaTime.now():
            return TlsObservation(
                host,
                "expired",
                local_expiry,
                hostname_valid,
                "TLS certificate has expired",
            )
        if not hostname_valid:
            return TlsObservation(
                host,
                "hostname_error",
                local_expiry,
                False,
                "TLS certificate does not match the hostname",
            )
        return TlsObservation(
            host, "valid", local_expiry, True, "TLS certificate valid"
        )

    def _certificate(self, host: str, port: int) -> bytes:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, port), timeout=10) as raw_socket:
            with context.wrap_socket(
                raw_socket, server_hostname=host
            ) as tls_socket:
                return tls_socket.getpeercert(binary_form=True)

    def _matches(self, host: str, certificate: x509.Certificate) -> bool:
        try:
            extension = certificate.extensions.get_extension_for_class(
                x509.SubjectAlternativeName
            )
            names = extension.value.get_values_for_type(x509.DNSName)
        except x509.ExtensionNotFound:
            names = []
        return any(self._match_name(host, name) for name in names)

    def _match_name(self, host: str, name: str) -> bool:
        if name.startswith("*."):
            suffix = name[1:].lower()
            return host.lower().endswith(suffix) and host.count(
                "."
            ) == name.count(".")
        return host.lower() == name.lower()
