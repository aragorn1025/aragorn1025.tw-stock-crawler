class TWSEDataError(Exception):
    def __init__(self):
        super().__init__("TWSE data invalid.")
