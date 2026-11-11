from datetime import date, datetime

from my_project.utils.errors import ApiError


def parse_date(value, field):
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        raise ApiError(f"Поле {field} має мати формат YYYY-MM-DD", 400)


def parse_dates_in(data, fields):
    for f in fields:
        if data.get(f) not in (None, ""):
            data[f] = parse_date(data[f], f)
        elif f in data:
            data[f] = None
    return data
