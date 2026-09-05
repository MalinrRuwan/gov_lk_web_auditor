import dns.exception
import dns.resolver

from ..models.MxObservation import MxObservation


class MxResolver:
    def resolve(self, domain: str, lifetime: float = 10.0) -> MxObservation:
        try:
            answer = dns.resolver.resolve(domain, "MX", lifetime=lifetime)
        except dns.resolver.NXDOMAIN:
            return MxObservation(
                domain,
                "no_mx",
                [],
                "The email domain does not resolve",
            )
        except (dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            return MxObservation(
                domain,
                "no_mx",
                [],
                "The email domain publishes no MX records",
            )
        except dns.resolver.LifetimeTimeout:
            return MxObservation(domain, "error", [], "The MX lookup timed out")
        except dns.exception.DNSException as error:
            return MxObservation(domain, "error", [], str(error))
        records = [
            (item.preference, item.exchange.to_text().rstrip("."))
            for item in answer
            if item.exchange.to_text().rstrip(".") != ""
        ]
        if not records:
            return MxObservation(
                domain,
                "no_mx",
                [],
                "The email domain publishes a null MX record (mail is rejected)",
            )
        return MxObservation(
            domain,
            "has_mx",
            records,
            f"Found {len(records)} MX record(s) for {domain}",
        )
