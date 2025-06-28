import datetime


def get_months(year: int) -> list[int]:
    today = datetime.date.today()
    if today.year < year:
        raise ValueError
    if today.year == year:
        return list(range(1, today.month + 1))
    return list(range(1, 12 + 1))
