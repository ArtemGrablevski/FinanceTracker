from aiogram.fsm.state import State, StatesGroup


class NewOperationState(StatesGroup):
    waiting_for_operation_date = State()
    waiting_for_operation_currency = State()
    waiting_for_operation_info = State()
