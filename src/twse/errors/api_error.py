class TWSEAPIError(Exception):
    def __init__(self):
        super().__init__("TWSE API failed.")
