from datetime import datetime


def date_to_readable_string(date: datetime) -> str:
    if date.hour == 0 and date.minute == 0 and date.second == 0 and date.microsecond == 0:
        return date.strftime("%d.%m.%y")
    return date.strftime("%H:%M %d.%m.%y")
