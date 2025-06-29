import datetime


def convert_roc_date(roc_date: str, separator: str = "/") -> datetime.date:
    roc_year, month, day = map(int, roc_date.split(separator))
    return datetime.date(roc_year + 1911, month, day)


def get_months(year: int) -> list[int]:
    today = datetime.date.today()
    if today.year < year:
        raise ValueError
    if today.year == year:
        return list(range(1, today.month + 1))
    return list(range(1, 12 + 1))
