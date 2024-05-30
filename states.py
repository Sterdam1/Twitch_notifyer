from aiogram.filters.state import State, StatesGroup

class ChooseState(StatesGroup):
    waiting_for_channel = State()
    waiting_for_twitch = State()
    
    
class ChangeState(StatesGroup):
    change_tg = State()
    change_twitch = State()

class FeedbackState(StatesGroup):
    waiting_for_feedback = State()
