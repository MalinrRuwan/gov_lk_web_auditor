# Implementation roadmap

This roadmap implements the criteria in [Grading Government Websites](article.md). Implement and test one level at a time. Do not begin a higher-level classifier until the preceding level produces reproducible evidence reports.

## Pre-levels — build the audit foundation

- [x] Define a versioned JSON schema for audits, evidence, and timestamps.
- [x] Build URL normalization, safe crawling, redirect tracking, page snapshots, and a per-site rate limit.
- [x] Build a report page and exportable JSON/CSV results.
- [x] Create test fixtures for live, dead, expired-certificate, parked, defaced, and redirected domains.

## Level 0: Empty Land — prove that the site is unavailable or unusable

Level 0 is the absence of Level 1. It has no independent action items or checks: a website is classified as Level 0 when the evidence cannot establish that it meets Level 1.

## Level 1: Nameboard — prove that the official site exists and works

Goal: reliably distinguish a current, authentic public website from a non-functional site, a temporary network problem, or a page that merely happens to load.

- [x] Detect when no site exists for the institution, including failed DNS and expired domains.
- [x] Test HTTP and HTTPS reachability, status codes, redirects, timeouts, and repeated availability.
- [x] Validate the TLS certificate, hostname, expiry date, and browser-blocking errors.
- [x] Detect parked domains, domain-squatter pages, generic hosting pages, defacement, hacking, and unrelated content.
- [x] Confirm reliable HTTPS loading under ordinary browser conditions.
- [x] Confirm that the site names and represents the expected institution.
- [x] Check domain plausibility, including `gov.lk`, while allowing legitimate government-owned exceptions.
- [x] Identify evidence that the site is maintained rather than abandoned.
- [x] Flag stale mirrors and contradictions between institutional identity, content, and domain.
- [x] Keep checks inconclusive when official status cannot be established automatically.
- [x] Return `pass`, `fail`, or `inconclusive`; transient failures must remain inconclusive.
- [x] Add regression tests for every failure mode that prevents Level 1.

## Level 2: Accessible Office — prove that citizens can reach the right office

Goal: determine whether the site helps a person find the correct physical or administrative doorway.

- [x] Find the correct postal address for the office a citizen would visit.
- [x] Find a phone number that is answered and an email address that is read.
- [x] Identify the division or officer responsible for each function.
- [x] Validate published contact syntax and consistency automatically.
- [x] Show the evidence by service, not only by the website as a whole.

## Level 3: Accessible Office with a Notice Board

Goal: find complete, current, usable instructions for each service.

- [ ] Crawl service pages and build a structured service catalogue.
- [x] Extract published eligibility criteria.
- [x] Find published required-document sections and certification references.
- [x] Extract published fees and payment methods.
- [x] Detect published legal-basis references.
- [ ] Link requirements to their legal basis and preserve superseded sources in an archive.
- [x] Extract expected processing times.
- [x] Find linked application forms with non-image document formats.
- [x] Capture visible update dates and fail dates older than two years.
- [ ] Compare regulated content with linked notices, documents, and counter practice.
- [ ] Measure Sinhala, Tamil, and English page availability, content equivalence, and freshness.
- [ ] Run mobile, performance, and low-bandwidth checks appropriate to inexpensive Android devices.
- [ ] Keep “complete checklist” and “current at the counter” inconclusive unless official structured data supports them.

## Level 4: Accessible Office, with a Notice Board, and a Working Counter

Goal: verify an end-to-end digital transaction without harming real users or systems.

- [ ] Verify online application submission and document upload.
- [ ] Verify online payment and generation of an accepted receipt.
- [ ] Verify status tracking.
- [ ] Verify delivery of a certificate, licence, or reasoned refusal.
- [ ] Verify published service standards, performance reports, and complaints that generate reference numbers.
- [ ] Trace service journeys using public pages and, only with explicit permission, sandbox/test accounts supplied by the agency.
- [ ] Record where a journey stops and why; never perform a real payment or submit a real application during an audit.
- [ ] Produce a per-service journey map so a single online form does not inflate the level of an entire institution.

## Level 5: Accessible Office, with a Notice Board, and a Working Counter which is motivated to help you succeed

Goal: identify real public-service infrastructure, not superficial AI features.

- [ ] Test whether free-text questions in Sinhala, Tamil, and English route people to the correct service across agencies.
- [ ] Verify that citizens are not asked for documents the state already holds.
- [ ] Detect published machine-readable eligibility rules and test them against real circumstances.
- [ ] Look for evidence that eligible citizens are proactively notified or offered entitlements.
- [ ] Verify automation disclosures, explanations for automated decisions, a named human appeal path, and accessible appeals information.
- [ ] Test structured open data and public APIs, including licences, formats, update frequency, and discoverability.
- [ ] Require strong machine-verifiable documentary evidence for every Level 5 claim.
