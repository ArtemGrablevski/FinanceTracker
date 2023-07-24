from typing import Literal
from datetime import datetime, timedelta

from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Operation
from models.operation import OperationDTO, OperationStatsDTO
from utils.date import date_to_readable_string


class OperationService:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_operation(
        self,
        user_id: int,
        operation_type: Literal["income", "expense"],
        amount: float,
        currency: Literal["USD", "EUR", "BYN", "PLN", "RUB", "USDT"],
        note: str,
        created_at: datetime
    ) -> None:
        amount_100x = round(amount * 100)
        await self.session.execute(
            insert(Operation).values(
                user_id=user_id,
                operation_type=operation_type,
                currency=currency,
                amount_100x=amount_100x,
                note=note,
                created_at=created_at
            )
        )
        await self.session.commit()

    async def get_operations_for_period(
        self,
        user_id: int,
        operation_type: Literal["income", "expense"],
        period_in_days: int
    ) -> OperationStatsDTO | None:

        sql_query = select(Operation).where(
            and_(
                Operation.user_id == user_id,
                Operation.operation_type == operation_type
            )
        ).order_by(Operation.created_at.desc())

        if period_in_days != 0:
            min_date = datetime.now() - timedelta(days=period_in_days)
            sql_query = sql_query.where(Operation.created_at > min_date)

        rows = await self.session.execute(sql_query)
        operations = rows.scalars().all()
        if not operations:
            return None

        total_amount = {}
        operations_history = []

        for operation in operations:

            amount = operation.amount_100x / 100
            amount = int(amount) if amount % 1 == 0 else amount
            currency = operation.currency
            date = date_to_readable_string(operation.created_at)

            total_amount[currency] = total_amount.get(currency, 0) + amount

            operations_history.append(
                OperationDTO(amount, currency, operation.note, date)
            )

        return OperationStatsDTO(operations_history, total_amount)
