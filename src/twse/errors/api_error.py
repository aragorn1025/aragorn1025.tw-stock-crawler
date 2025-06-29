"""TWSE API error."""


class TWSEAPIError(Exception):
    """Raised if the TWSE API fails."""

    def __init__(self):
        super().__init__("TWSE API failed.")
