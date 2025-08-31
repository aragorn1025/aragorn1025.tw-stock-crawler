"""Utility functions."""

import datetime


def convert_roc_date(roc_date: str, separator: str = "/") -> datetime.date:
    """Convert ROC date string to a datetime.date object.
    Parameters:
        roc_date (str):
            Date in ROC format separated by slashes (e.g., "111/01/01").
        separator (str):
            The separator used in the ROC date string. Default is "/".
    Returns:
        datetime.date:
            Corresponding date in Gregorian calendar.
    """
    roc_year, month, day = map(int, roc_date.split(separator))
    return datetime.date(roc_year + 1911, month, day)


def get_year() -> int:
    """Get the current year in AD.
    Returns:
        int:
            The current year in AD.
    """
    return datetime.date.today().year


def get_months(year: int) -> list[int]:
    """Get the months available for a given year.
    Parameters:
        year (int):
            The year to get the months for.
    Returns:
        list[int]:
            A list of months available for the given year.
    """
    today = datetime.date.today()
    if today.year < year:
        raise ValueError
    if today.year == year:
        return list(range(1, today.month + 1))
    return list(range(1, 12 + 1))
