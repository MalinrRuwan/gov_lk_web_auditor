import ipaddress
import socket

from ..models.DnsObservation import DnsObservation


class DnsResolver:
    def resolve(self, host: str) -> DnsObservation:
        try:
            records = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
        except socket.gaierror as error:
            absent = error.errno in {socket.EAI_NONAME, socket.EAI_NODATA}
            status = "absent" if absent else "error"
            return DnsObservation(host, [], status, str(error))
        return self._observation(host, records)

    def _observation(self, host: str, records: list) -> DnsObservation:
        addresses = sorted({record[4][0] for record in records})
        if not addresses:
            return DnsObservation(host, [], "absent", "No addresses returned")
        if any(not self._is_public(address) for address in addresses):
            detail = "DNS resolved to a non-public address; crawling blocked"
            return DnsObservation(host, addresses, "blocked", detail)
        return DnsObservation(
            host, addresses, "resolved", "Public DNS resolved"
        )

    def _is_public(self, address: str) -> bool:
        parsed = ipaddress.ip_address(address)
        return parsed.is_global
