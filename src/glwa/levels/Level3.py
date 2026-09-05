from ..checks.level3 import EvidenceCheck
from .Level import Level


class Level3(Level):
    def __init__(self):
        checks = (
            EvidenceCheck("eligibility_criteria", "Eligibility criteria"),
            EvidenceCheck("required_documents", "Required documents"),
            EvidenceCheck("fees_and_payment", "Fees and payment"),
            EvidenceCheck("legal_basis", "Legal basis"),
            EvidenceCheck("processing_time", "Processing time"),
            EvidenceCheck("downloadable_form", "Downloadable form"),
            EvidenceCheck("published_update_date", "Published update date"),
        )
        super().__init__(
            3,
            "To pass `Level 3`, citizens must find complete and current "
            "instructions, requirements, fees, times, and usable forms.",
            checks,
        )
