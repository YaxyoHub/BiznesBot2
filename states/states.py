from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    name = State()
    phone = State()
    business = State()

class AddAdmin(StatesGroup):
    name = State()
    username = State()
    phone = State()
    id = State()

class DeleteAdmin(StatesGroup):
    id = State()

class SendMessage(StatesGroup):
    waiting_message = State()