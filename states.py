from aiogram.filters.state import State, StatesGroup

class EmailState(StatesGroup):
    waiting_for_email = State()