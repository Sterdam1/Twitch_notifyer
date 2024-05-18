from aiogram.filters.state import State, StatesGroup

class ChooseState(StatesGroup):
    waiting_for_channel = State()
    waiting_for_twitch = State()
    null = State()