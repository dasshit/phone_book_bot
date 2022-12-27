from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    """
    Стейты пользовалея
    """
    USER_DB_ID = State()

    INITIAL_STATE = State()

    IMPORT_CONTACT_START = State()

    IMPORT_CONTACT_BY_PARTS = State()
    ENTER_FIRST_NAME = State()
    ENTER_LAST_NAME = State()
    ENTER_PHONE = State()
    ENTER_CONTACT_TYPE = State()

    IMPORT_CONTACT_BY_CARD = State()

    SHOW_CONTACT = State()
    SHOW_CONTACT_MULTILINE = State()
    SHOW_CONTACT_CARD = State()

    DELETE_CONTACT = State()
