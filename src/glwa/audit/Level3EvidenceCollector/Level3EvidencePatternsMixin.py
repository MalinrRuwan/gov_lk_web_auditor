import re


class Level3EvidencePatternsMixin:
    SIGNALS = {
        "eligibility_criteria": (
            "eligibility",
            "eligible applicants",
            "who can apply",
        ),
        "required_documents": (
            "required documents",
            "documents required",
            "supporting documents",
            "document checklist",
        ),
        "legal_basis": (
            "legal basis",
            "under the act",
            "regulations",
            "gazette",
            "circular",
        ),
    }
    MONEY = re.compile(r"(?:rs\.?|lkr|රු\.?|ரூ\.?)\s*[\d,]+", re.I)
    FREE = re.compile(
        r"\b(?:free of charge|no fee|fee is not charged)\b", re.I
    )
    PAYMENT = ("payment", "payable", "cash", "bank", "online payment")
    DURATION = re.compile(
        r"\b\d+\s*(?:(?:working|business|calendar)\s+)?"
        r"(?:hours?|days?|weeks?|months?)\b",
        re.I,
    )
    TIME = ("processing time", "service time", "within", "takes")
    DATE = re.compile(
        r"\b(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[/-]\d{1,2}[/-]\d{4}|"
        r"\d{1,2}\s+[a-z]+\s+\d{4})\b",
        re.I,
    )
    UPDATED = ("last updated", "updated on", "last modified", "as of")
    FORM_EXTENSIONS = (".pdf", ".doc", ".docx", ".odt")
