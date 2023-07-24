from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class OperationDTO:

    amount: int | float
    currency: Literal["USD", "EUR", "BYN", "PLN", "RUB", "USDT"]
    note: str
    date: str

    def to_html_string(self) -> str:
        return f"{self.note}: <b>{self.amount} {self.currency}</b> ({self.date})"


@dataclass
class OperationStatsDTO:

    operations: list[OperationDTO]
    total_amount: dict[
        Literal["USD", "EUR", "BYN", "PLN", "RUB", "USDT"], int | float
    ]

    def to_html_string(self) -> str:
        total = ", ".join(
            [f"<b>{self.total_amount[currency]} {currency}</b>" for currency in self.total_amount]
        )
        operations_history = "\n\n".join(
            ["🔹 " + op.to_html_string() for op in self.operations]
        )
        return f"💰 Total: {total}\n\n{operations_history}"
