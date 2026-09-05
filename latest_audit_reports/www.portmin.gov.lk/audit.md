# Website Audit: http://www.portmin.gov.lk/

- Completed: 2026-09-05 11:34
- Overall result: 🔴 Level 1

## ⚫ Level 0: ✅

A site is classified as `⚫ Level 0` when it is unavailable or unusable, or when there is not enough evidence to establish that it meets `🔴 Level 1`.

Baseline website grade

## 🔴 Level 1: ✅

To pass `🔴 Level 1`, the website must be available, usable, and clearly associated with the government institution. It must load reliably with valid DNS, HTTP, and TLS behavior.

TLS certificate expired but the site remains available; kept at 🔴 Level 1

| Test | Result | Details |
| --- | --- | --- |
| dns_resolves | ✅ | Public DNS resolved |
| domain_not_parked | ✅ | No parked-domain marker found |
| site_not_defaced | ✅ | No defacement marker found |
| content_relevant | ✅ | No unrelated-content marker found |
| hosting_configured | ✅ | No generic-hosting marker found |
| http_available | ✅ | HTTP probes did not all fail |
| redirect_related | ✅ | No unrelated redirect found |
| tls_browser_trusted | ❌ | Probe 1: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1000) |
| tls_not_expired | ❌ | TLS certificate has expired |
| tls_hostname_matches | ❓ | TLS hostname check did not run |

## 🟠 Level 2: ❓

To pass `🟠 Level 2`, citizens must be able to identify and contact the correct office for the service they need.

No passing postal address evidence found; No phone or email evidence found; No passing named responsibility evidence found; No passing email on the site domain evidence found; No passing email domain has mx records evidence found

| Test | Result | Details |
| --- | --- | --- |
| postal_address | ❓ | No passing postal address evidence found |
| reachable_contacts | ❓ | No phone or email evidence found |
| named_responsibility | ❓ | No passing named responsibility evidence found |
| email_in_site_domain | ❓ | No passing email on the site domain evidence found |
| email_domain_has_mx | ❓ | No passing email domain has mx records evidence found |

## 🟢 Level 3: ❓

To pass `🟢 Level 3`, citizens must find complete and current instructions, requirements, fees, times, and usable forms.

Not run because 🟠 Level 2 did not pass
