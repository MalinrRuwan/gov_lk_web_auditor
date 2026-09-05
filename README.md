# Grading Government Websites (`glwa`)

[![MIT License](https://img.shields.io/github/license/nuuuwan/glwa)](LICENSE) [![Author](https://img.shields.io/badge/author-nuuuwan-181717?logo=github)](https://github.com/nuuuwan) ![Last updated](https://img.shields.io/badge/last_updated-2026--09--05_12%3A24_SLST-007ec6)

`glwa` audits Sri Lankan government websites using an evidence-based, cumulative grading model. It records reproducible evidence for each level and publishes the latest classification and audit report for every website in Sri Lanka. 🇱🇰

> **Implementation status:** Only `⚫ Level 0`, `🔴 Level 1`, `🟠 Level 2`, and `🟢 Level 3` are implemented.

## Levels and scoring

| Level | Implemented | Description |
| --- | :---: | --- |
| `⚫ Level 0` | ✅ Yes | A site is classified as `⚫ Level 0` when it is unavailable or unusable, or when there is not enough evidence to establish that it meets `🔴 Level 1`. |
| `🔴 Level 1` | ✅ Yes | The website must be available, usable, and clearly associated with the government institution. It must load reliably with valid DNS, HTTP, and TLS behavior. |
| `🟠 Level 2` | ✅ Yes | Citizens must be able to identify and contact the correct office for the service they need. |
| `🟢 Level 3` | ✅ Yes | Citizens must find complete and current instructions, requirements, fees, times, and usable forms. |
| `🔵 Level 4` | ❌ No | Citizens must be able to complete, pay for, track, and receive the outcome of a service online. |
| `🟣 Level 5` | ❌ No | Services must be connected across agencies, proactive for eligible citizens, explainable, and accountable. |

The score is out of 3. `🔴 Level 1` through `🟢 Level 3` each contribute up to 1 point, calculated as passing checks divided by total checks. `⚫ Level 0` contributes no points. The total is shown to one decimal place.

## Sites by level

```mermaid
%%{init: {"themeVariables":{"pie1":"black","pie2":"red","pie3":"orange","pie4":"green"}}}%%
pie showData
    title Sites by level
    "⚫ Level 0" : 5
    "🔴 Level 1" : 14
    "🟠 Level 2" : 0
    "🟢 Level 3" : 0
```

## Documentation

- [Article](docs/article.md): The grading framework.
- [Design](docs/design.md): Architecture and rules.
- [Roadmap](docs/roadmap.md): Work completed and planned.

## `⚫ Level 0`

**5 URLs at `⚫ Level 0`.**

Checks used: Availability and usability checks.

| Score | URL |
| ---: | --- |
| 0.1/3 | [https://www.powermin.gov.lk/](latest_audit_reports/www.powermin.gov.lk/audit.md) |
| 0.3/3 | [https://www.presidentsfund.gov.lk/](latest_audit_reports/www.presidentsfund.gov.lk/audit.md) |
| 0.7/3 | [http://www.irrigationmin.gov.lk/](latest_audit_reports/www.irrigationmin.gov.lk/audit.md) |
| 0.7/3 | [https://www.moys.gov.lk/](latest_audit_reports/www.moys.gov.lk/audit.md) |
| 0.9/3 | [https://www.moha.gov.lk/](latest_audit_reports/www.moha.gov.lk/audit.md) |

## `🔴 Level 1`

**14 URLs at `🔴 Level 1`.**

Checks used: DNS resolves, Domain not parked, Site not defaced, Content relevant, Hosting configured, HTTP available, Redirect related, TLS browser trusted, TLS not expired, TLS hostname matches.

| Score | URL |
| ---: | --- |
| 0.1/3 | [https://www.energymin.gov.lk/](latest_audit_reports/www.energymin.gov.lk/audit.md) |
| 0.1/3 | [https://www.mrds.gov.lk/](latest_audit_reports/www.mrds.gov.lk/audit.md) |
| 0.7/3 | [http://www.portmin.gov.lk/](latest_audit_reports/www.portmin.gov.lk/audit.md) |
| 1.4/3 | [https://cleansrilanka.gov.lk/](latest_audit_reports/cleansrilanka.gov.lk/audit.md) |
| 1.4/3 | [https://rebuildingsrilanka.gov.lk/](latest_audit_reports/rebuildingsrilanka.gov.lk/audit.md) |
| 1.6/3 | [https://elections.gov.lk/](latest_audit_reports/elections.gov.lk/audit.md) |
| 1.6/3 | [https://landmin.gov.lk/](latest_audit_reports/landmin.gov.lk/audit.md) |
| 1.6/3 | [https://most.gov.lk/](latest_audit_reports/most.gov.lk/audit.md) |
| 1.6/3 | [https://mpclg.gov.lk/](latest_audit_reports/mpclg.gov.lk/audit.md) |
| 1.6/3 | [https://www.env.gov.lk/](latest_audit_reports/www.env.gov.lk/audit.md) |
| 1.6/3 | [https://www.moudh.gov.lk/](latest_audit_reports/www.moudh.gov.lk/audit.md) |
| 1.8/3 | [https://www.agrimin.gov.lk/](latest_audit_reports/www.agrimin.gov.lk/audit.md) |
| 1.8/3 | [https://www.presidentsoffice.gov.lk/](latest_audit_reports/www.presidentsoffice.gov.lk/audit.md) |
| 1.8/3 | [https://www.pubad.gov.lk/](latest_audit_reports/www.pubad.gov.lk/audit.md) |

## `🟠 Level 2`

**0 URLs at `🟠 Level 2`.**

Checks used: Postal address, Reachable contacts, Named responsibility, Email in site domain, Email domain has mx.

## `🟢 Level 3`

**0 URLs at `🟢 Level 3`.**

Checks used: Eligibility criteria, Required documents, Fees and payment, Legal basis, Processing time, Downloadable form, Published update date.
