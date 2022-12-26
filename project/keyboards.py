from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

from project.enums import UserTextCommandsEnum


CHOOSE_OPERATION_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=UserTextCommandsEnum.WRITE_CONTACT)],
        [KeyboardButton(text=UserTextCommandsEnum.SHOW_CONTACT)],
        [KeyboardButton(text=UserTextCommandsEnum.DELETE_CONTACT)],
        [KeyboardButton(text=UserTextCommandsEnum.SHOW_CONTACT_FILE)],
    ],
    resize_keyboard=True,
    input_field_placeholder=UserTextCommandsEnum.PLACEHOLDER
)

CHOOSE_CONTACT_VIEW_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=UserTextCommandsEnum.SHOW_CONTACT_ONE_LINE)],
        [KeyboardButton(text=UserTextCommandsEnum.SHOW_CONTACT_MULTI_LINE)],
        [KeyboardButton(text=UserTextCommandsEnum.BACK)],
    ],
    resize_keyboard=True,
    input_field_placeholder=UserTextCommandsEnum.PLACEHOLDER
)


BACK_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=UserTextCommandsEnum.BACK)],
    ],
    resize_keyboard=True,
    input_field_placeholder=UserTextCommandsEnum.PLACEHOLDER
)
