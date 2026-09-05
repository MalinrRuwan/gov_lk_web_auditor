from .Level import Level


class Level4(Level):
    def __init__(self):
        super().__init__(
            4,
            "To pass `Level 4`, citizens must be able to complete, pay for, "
            "track, and receive the outcome of a service online.",
        )
