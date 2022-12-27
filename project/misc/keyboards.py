from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

from project.misc.enums import UserTextCommandsEnum


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


ENTER_CONTACT_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=UserTextCommandsEnum.WRITE_CONTACT_BY_PARTS)],
        [KeyboardButton(text=UserTextCommandsEnum.WRITE_CONTACT_BY_CARD)],
        [KeyboardButton(text=UserTextCommandsEnum.BACK)],
    ],
    resize_keyboard=True,
    input_field_placeholder=UserTextCommandsEnum.PLACEHOLDER
)


SHOW_CONTACT_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=UserTextCommandsEnum.SHOW_CONTACT_MULTI_LINE)],
        [KeyboardButton(text=UserTextCommandsEnum.SHOW_CONTACT_VCARD)],
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
