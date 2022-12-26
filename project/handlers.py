import os.path
import typing

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.handlers import ErrorHandler
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.filters.command import Command

from project.enums import BotTextEnum, UserTextCommandsEnum
from project.keyboards import log_in_out_keyboard, logout_keyboard
from project import text_handler
from project.logger import logger


router = Router()


class UserState(StatesGroup):
    choose_operation_type = State()
    delete_contact = State()
    get_file = State()
    log_in_operation = State()
    log_out_operation = State()
    log_out_one_line = State()
    log_out_lines = State()


@router.errors()
class MyHandler(ErrorHandler):
    async def handle(self) -> typing.Any:
        logger.exception(
            "Cause unexpected exception %s: %s",
            self.exception_name,
            self.exception_message
        )
        await self.bot.send_message(
            chat_id=self.event.update.message.chat.id,
            text=BotTextEnum.ERROR_TEXT.format(self.event.exception),
            reply_to_message_id=self.event.update.message.message_id,
            reply_markup=log_in_out_keyboard
        )
        await self.data['state'].set_state(UserState.choose_operation_type)


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        text=BotTextEnum.WELCOME_TEXT,
        reply_markup=log_in_out_keyboard
    )
    await state.set_state(UserState.choose_operation_type)


@router.message(
    UserState.choose_operation_type,
    Text(text=UserTextCommandsEnum.WRITE_CONTACT.value)
)
async def choose_operation(message: Message, state: FSMContext):

    await message.reply(
        text=BotTextEnum.ENTER_CONTACT,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.log_in_operation)


@router.message(
    UserState.choose_operation_type,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT.value)
)
async def choose_operation(message: Message, state: FSMContext):
    assert os.path.exists(
        text_handler.get_phone_book_path(message.chat.username)), \
        "Запишите хотя бы один контакт, книга пуста"
    await message.answer(
        text=BotTextEnum.CHOOSE_OUTPUT_FORMAT,
        reply_markup=logout_keyboard
    )
    await state.set_state(UserState.log_out_operation)


@router.message(
    UserState.choose_operation_type,
    Text(text=UserTextCommandsEnum.DELETE_CONTACT.value)
)
async def choose_operation(message: Message, state: FSMContext):
    assert os.path.exists(
        text_handler.get_phone_book_path(message.chat.username)), \
        "Запишите хотя бы один контакт, книга пуста"
    await message.answer(
        text=BotTextEnum.ENTER_NUMBER_TO_DELETE_CONTACT,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.delete_contact)


@router.message(
    UserState.choose_operation_type,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT_FILE.value)
)
async def choose_operation(message: Message, state: FSMContext):
    phone_book_path = text_handler.get_phone_book_path(message.chat.username)

    assert os.path.exists(phone_book_path), \
        "Запишите хотя бы один контакт, книга пуста"
    await message.reply_document(FSInputFile(phone_book_path))


@router.message(UserState.log_in_operation)
async def log_in_operation(message: Message, state: FSMContext):
    if message.text:
        text_handler.write_line(
            line=text_handler.checked_handle_line(
                message.text
            ),
            user_name=message.chat.username
        )
    else:
        text_handler.handle_contact(
            contact=message.contact, user_name=message.chat.username
        )

    await message.answer(
        text=BotTextEnum.ADD_CONTACT_SUCCESS,
        reply_markup=log_in_out_keyboard
    )
    await state.set_state(UserState.choose_operation_type)


@router.message(
    UserState.log_out_operation,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT_ONE_LINE.value)
)
async def log_out_operation(message: Message, state: FSMContext):
    await message.answer(
        text=BotTextEnum.ENTER_CONTACT_NAME,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.log_out_one_line)


@router.message(
    UserState.log_out_operation,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT_MULTI_LINE.value)
)
async def log_out_operation(message: Message, state: FSMContext):

    await message.answer(
        text=BotTextEnum.ENTER_CONTACT_NAME,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.log_out_lines)


@router.message(
    UserState.log_out_operation,
    Text(text=UserTextCommandsEnum.BACK.value)
)
async def log_out_operation(message: Message, state: FSMContext):
    await message.answer(
        text=BotTextEnum.COMMIN_BACK,
        reply_markup=log_in_out_keyboard
    )
    await state.set_state(UserState.choose_operation_type)


@router.message(UserState.log_out_one_line)
async def logging_out_one_line(message: Message, state: FSMContext):
    await message.answer(
        text=', '.join(text_handler.find_line(
            line=message.text,
            user_name=message.chat.username
        )),
        reply_markup=log_in_out_keyboard
    )
    await state.set_state(UserState.choose_operation_type)


@router.message(UserState.log_out_lines)
async def logging_out_lines(message: Message, state: FSMContext):
    first_name, last_name, phone, misc = text_handler.find_line(
        line=message.text,
        user_name=message.chat.username
    )
    await message.answer_contact(
        phone_number=phone,
        first_name=first_name,
        last_name=last_name,
        reply_markup=log_in_out_keyboard
    )
    await state.set_state(UserState.choose_operation_type)


@router.message(UserState.delete_contact)
async def delete_contact(message: Message, state: FSMContext):
    text_handler.delete_line(message.text, message.chat.username)
    await message.answer(
        text=BotTextEnum.AFTER_SUCCESS_DELETE,
        reply_markup=log_in_out_keyboard
    )
    await state.set_state(UserState.choose_operation_type)
