from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class OperationInfoMessage:
    amount: float
    note: str


def parse_operation_info_message(message: str) -> OperationInfoMessage:

    whitespace_index = message.find(" ")

    if whitespace_index == -1:
        raise ValueError("Invalid message format!")

    amount = message[:whitespace_index]

    if not amount.isdigit():
        if not amount.replace(".", "").isdigit() or len(str(amount).split(".")[1]) not in (0, 1, 2):
            raise ValueError("Invalid operation amount!")

    if float(amount) < 0:
        raise ValueError("Invalid operation amount!")

    note = message[whitespace_index + 1:]
    return OperationInfoMessage(float(amount), note)


def parse_datetime_message(message: str) -> datetime:
    if ":" in message:
        return datetime.strptime(message, "%H:%M %d.%m.%y")
    return datetime.strptime(message, "%d.%m.%y")
