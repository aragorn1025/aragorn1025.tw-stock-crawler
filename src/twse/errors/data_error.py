"""TWSE data error."""


class TWSEDataError(Exception):
    """Raised if the TWSE data is invalid."""

    def __init__(self):
        super().__init__("TWSE data invalid.")
