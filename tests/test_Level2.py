import unittest

from glwa.levels.Level2 import Level2
from glwa.models.Evidence import Evidence


class TestLevel2(unittest.TestCase):
    def setUp(self):
        self.level = Level2()

    def test_passes_confirmed_complete_contact_evidence(self):
        result = self.level.run(self._complete_evidence())
        self.assertEqual("pass", result.status)
        self.assertEqual(5, len(result.checks))
        contacts = next(
            item for item in result.checks if item.name == "reachable_contacts"
        )
        self.assertEqual(
            "Phone: +94 11 234 5678 (2 phone numbers found); "
            "Email: help@example.gov.lk (2 email addresses found)",
            contacts.reason,
        )

    def test_email_domain_checks_report_domain_and_mx_outcomes(self):
        result = self.level.run(
            self._complete_evidence()
            + [
                Evidence(
                    "email_in_site_domain",
                    "fail",
                    "Email domain not part of the site domain",
                ),
                Evidence(
                    "email_domain_has_mx",
                    "pass",
                    "Found 1 MX record(s) for example.gov.lk",
                ),
            ]
        )
        owner = next(
            item for item in result.checks if item.name == "email_in_site_domain"
        )
        mx = next(item for item in result.checks if item.name == "email_domain_has_mx")
        self.assertEqual("fail", owner.status)
        self.assertEqual("pass", mx.status)
        self.assertEqual("fail", result.status)

    def test_is_inconclusive_when_evidence_is_missing(self):
        result = self.level.run([])
        self.assertEqual("inconclusive", result.status)

    def test_review_contacts_do_not_pass(self):
        evidence = [
            Evidence("phone", "review", "Phone number found"),
            Evidence("email", "review", "Email address found"),
        ]
        result = self.level.run(evidence)
        contacts = next(
            item for item in result.checks if item.name == "reachable_contacts"
        )
        self.assertEqual("inconclusive", contacts.status)
        self.assertNotIn("human", contacts.reason.lower())

    def _complete_evidence(self):
        return [
            Evidence("postal_address", "pass", "Address confirmed"),
            self._contact("phone", "+94 11 234 5678"),
            self._contact("phone", "+94 11 765 4321"),
            self._contact("phone", "+94 11 234 5678"),
            self._contact("email", "help@example.gov.lk"),
            self._contact("email", "info@example.gov.lk"),
            self._contact("email", "help@example.gov.lk"),
            Evidence("named_responsibility", "pass", "Officer named"),
            Evidence("email_in_site_domain", "pass", "Email on the site domain"),
            Evidence("email_domain_has_mx", "pass", "Email domain has MX records"),
        ]

    def _contact(self, name, value):
        return Evidence(
            name,
            "pass",
            f"Published {name}",
            data={"value": value},
        )


if __name__ == "__main__":
    unittest.main()
