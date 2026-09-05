from ..checks.level2 import EvidenceCheck, ReachableContactsCheck
from .Level import Level


class Level2(Level):
    def __init__(self):
        checks = (
            EvidenceCheck("postal_address", "Postal address"),
            ReachableContactsCheck(),
            EvidenceCheck("named_responsibility", "Named responsibility"),
        )
        super().__init__(
            2,
            "To pass `Level 2`, citizens must be able to identify and "
            "contact the correct office for the service they need.",
            checks,
        )
