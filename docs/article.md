# Grading Government Websites

## Level 0 to Level 5, inspired by a citizen-led audit

*By Nuwan I. Senaratna"

*Originally shared at <https://medium.com/on-technology/grading-government-websites-d55c7dddb412>*

The Lanka Data Foundation is running a Government Website Scorecard Hackathon on the 5th of September (2026), a citizen-led audit of government websites. It is an excellent project. Nobody has ever measured this systematically, so there is no baseline against which anything can be shown to improve or decay.

It also raises a broader question.

> What is a government website meant to do?

For me, it is primarily one thing: lower the cost of processes, citizens are entitled to. The passport, the pension, the permit, the land record. The website does not grant the right; the law does. But the website could decide how much time, bus fare and lost wages you spend claiming it.

And so in this article, I attempt to define a grading system for state websites, from Level 0 to Level 5.

## Level 0: Empty Land

The website doesn’t exist or doesn’t work. One or more of the following is true:

1. No site exists for the institution at all.
2. The domain has expired, or lapsed to a squatter.
3. The server is down, or has been down long enough that nobody noticed.
4. The TLS certificate expired and the browser now blocks entry.
5. The page is parked, defaced, hacked, or serving something unrelated.

Technically these are different failures. For the citizen standing at the other end they are the same one. Like you went to the address of a government department, and there was no building there.

## Level 1: Nameboard

The site is up and it is genuinely the official one. What it adds above Level 0 is:

1. It loads reliably, over HTTPS, on a normal connection.
2. It names the institution, and it is clear this is the real one rather than a copy or an abandoned older version.
3. It sits on a plausible official domain, ideally gov.lk.
4. A human has touched it in living memory.

Beyond that, it may be pure publicity: The minister’s photograph, a vision statement, a ribbon cutting from 2019.

You have found the right building and the board out front confirms it. But you can’t go in. Not much more useful than an empty plot.

## Level 2: Accessible Office

What Level 2 adds above Level 1:

1. A correct postal address for the office you would actually visit.
2. A phone number somebody answers, and an email somebody reads.
3. A named division or officer responsible for each function, rather than one generic contact page.

The guard cannot process anything for you. He tells you the third floor, after two, and that pensions are a different building entirely. That is a surprisingly large share of the misery involved in dealing with the state.

## Level 3: Accessible Office with a Notice Board

Everything a citizen needs to prepare, and enough evidence to trust it. Beyond Level 2, Level 3 adds:

1. Eligibility criteria in plain language.
2. The complete document checklist, including which copies must be certified and by whom.
3. The fee as an accurate and up-to-date number, and how it may be paid.
4. The legal basis: the act, regulation or circular the requirement comes from, with the superseded ones archived rather than deleted.
5. Expected processing time.
6. The forms themselves, downloadable, as real files rather than photographs of paper.
7. A visible last-updated date on every page carrying a fee, a rule or a form, and content that actually matches what the counter uses today.
8. Sinhala, Tamil and English at equal quality and equal freshness, usable on a cheap Android phone over a patchy connection.

## Level 4: Accessible Office, with a Notice Board, and a Working Counter

What it adds above Level 3:

1. Submit the application online, with document upload.
2. Pay online, and receive a receipt that is accepted as proof.
3. Track status, so nobody has to ring up and ask where their file is sitting.
4. Receive the outcome, whether that is a certificate, a licence or a refusal with reasons.
5. Published service standards with actual performance against them, and complaints that generate a reference number.

## Level 5: Accessible Office, with a Notice Board, and a Working Counter which is motivated to help you succeed

This is where modern tooling earns its keep, if it is used seriously rather than just bolted on:

1. You describe your problem in your own words, in any of the three languages, and are routed to the right service across departments. Most citizens do not know whether their question belongs to the Divisional Secretariat or the Land Registry, and should not have to.
2. Documents the state already holds are never requested again. -  Interoperability first; a form that asks for your birth certificate is a system admitting it cannot talk to the Registrar General.
3. The rules are machine readable, so eligibility can be checked against your actual circumstances rather than explained in general terms.
4. The state tells you what you are owed before you ask. If a registered birth entitles a household to a grant, the grant is offered, not advertised and waited on.
5. Every automated decision is explainable and appealable to a named human, and it is disclosed when a system rather than an officer decided.
6. Structured open data and public APIs, so others can build things the department never would.

Note what is *not* on that list. A chatbot answering FAQs on a site whose fee schedule is from 2019 is not Level 5, it is Level 1 wearing a fancy costume. AI here is only worth anything when the underlying records, rules and registries are good enough to reason over, which is why the levels are cumulative.
