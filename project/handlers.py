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
from project.keyboards import CHOOSE_OPERATION_KEYBOARD, CHOOSE_CONTACT_VIEW_KEYBOARD, BACK_KEYBOARD
from project import text_handler


router = Router()


class UserState(StatesGroup):
    """
    Стейты пользовалея
    """
    CHOOSE_NEXT_OPERATION = State()
    WRITE_CONTACT = State()
    SHOW_CONTACT = State()
    SHOW_CONTACT_ONE_LINE = State()
    SHOW_CONTACT_MULTI_LINE = State()
    DELETE_CONTACT = State()
    SEND_PHONE_BOOK_FILE = State()


@router.errors()
class RouterErrorHandler(ErrorHandler):
    async def handle(self):
        """
        Обработчик ошибок в хэндлерах бота
        """
        await self.bot.send_message(
            chat_id=self.event.update.message.chat.id,
            text=BotTextEnum.ERROR_TEXT.format(self.event.exception),
            reply_to_message_id=self.event.update.message.message_id,
            reply_markup=CHOOSE_OPERATION_KEYBOARD
        )
        await self.data['state'].set_state(UserState.CHOOSE_NEXT_OPERATION)


@router.message(
    Text(text=UserTextCommandsEnum.BACK.value)
)
async def comming_back(message: Message, state: FSMContext):
    """
    Обработка комманды 'Назад'
    """
    await message.answer(
        text=BotTextEnum.COMMIN_BACK,
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )
    await state.set_state(UserState.CHOOSE_NEXT_OPERATION)


@router.message(Command('start'))
async def command_start(message: Message, state: FSMContext):
    """
    Обработка комманды '/start'
    """
    await message.answer(
        text=BotTextEnum.WELCOME_TEXT,
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )
    await state.set_state(UserState.CHOOSE_NEXT_OPERATION)


@router.message(
    UserState.CHOOSE_NEXT_OPERATION,
    Text(text=UserTextCommandsEnum.WRITE_CONTACT.value)
)
async def choose_write_contact(message: Message, state: FSMContext):
    """
    Обработка комманды 'Записать контакт'
    """
    await message.reply(
        text=BotTextEnum.ENTER_CONTACT,
        reply_markup=BACK_KEYBOARD
    )
    await state.set_state(UserState.WRITE_CONTACT)


@router.message(
    UserState.CHOOSE_NEXT_OPERATION,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT.value)
)
async def choose_show_contact(message: Message, state: FSMContext):
    """
    Обработка комманды 'Посмотреть контакт'
    """
    assert os.path.exists(
        text_handler.get_phone_book_path(message.chat.username)), \
        "Запишите хотя бы один контакт, книга пуста"
    await message.answer(
        text=BotTextEnum.CHOOSE_OUTPUT_FORMAT,
        reply_markup=CHOOSE_CONTACT_VIEW_KEYBOARD
    )
    await state.set_state(UserState.SHOW_CONTACT)


@router.message(
    UserState.CHOOSE_NEXT_OPERATION,
    Text(text=UserTextCommandsEnum.DELETE_CONTACT.value)
)
async def choose_delete_contact(message: Message, state: FSMContext):
    """
    Обработка комманды 'Удалить контакт'
    """
    assert os.path.exists(
        text_handler.get_phone_book_path(message.chat.username)), \
        "Запишите хотя бы один контакт, книга пуста"
    await message.answer(
        text=BotTextEnum.ENTER_NUMBER_TO_DELETE_CONTACT,
        reply_markup=BACK_KEYBOARD
    )
    await state.set_state(UserState.DELETE_CONTACT)


@router.message(
    UserState.CHOOSE_NEXT_OPERATION,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT_FILE.value)
)
async def choose_show_contact_file(message: Message, state: FSMContext):
    """
    Обработка комманды 'Показать файл'
    """
    phone_book_path = text_handler.get_phone_book_path(message.chat.username)

    assert os.path.exists(phone_book_path), \
        "Запишите хотя бы один контакт, книга пуста"
    await message.reply_document(FSInputFile(phone_book_path))


@router.message(UserState.WRITE_CONTACT)
async def write_contact(message: Message, state: FSMContext):
    """
    Обработка стейта WRITE_CONTACT
    """
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
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )
    await state.set_state(UserState.CHOOSE_NEXT_OPERATION)


@router.message(
    UserState.SHOW_CONTACT,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT_ONE_LINE.value)
)
async def show_contact_one_line(message: Message, state: FSMContext):
    """
    Обработка команды 'Показать контакт одной строкой'
    """
    await message.answer(
        text=BotTextEnum.ENTER_CONTACT_NAME,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.SHOW_CONTACT_ONE_LINE)


@router.message(
    UserState.SHOW_CONTACT,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT_MULTI_LINE.value)
)
async def show_contact_card(message: Message, state: FSMContext):
    """
    Обработка команды 'Показать контакт в несколько строк'
    """
    await message.answer(
        text=BotTextEnum.ENTER_CONTACT_NAME,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.SHOW_CONTACT_MULTI_LINE)


@router.message(UserState.SHOW_CONTACT_ONE_LINE)
async def show_contact_one_line_final(message: Message, state: FSMContext):
    """
    Обработка стейта SHOW_CONTACT_ONE_LINE
    """
    await message.answer(
        text=', '.join(text_handler.find_line(
            line=message.text,
            user_name=message.chat.username
        )),
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )
    await state.set_state(UserState.CHOOSE_NEXT_OPERATION)


@router.message(UserState.SHOW_CONTACT_MULTI_LINE)
async def show_contact_card_final(message: Message, state: FSMContext):
    """
    Обработка стейта SHOW_CONTACT_MULTI_LINE
    """
    first_name, last_name, phone, misc = text_handler.find_line(
        line=message.text,
        user_name=message.chat.username
    )
    await message.answer_contact(
        phone_number=phone,
        first_name=first_name,
        last_name=last_name,
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )
    await state.set_state(UserState.CHOOSE_NEXT_OPERATION)


@router.message(UserState.DELETE_CONTACT)
async def delete_contact(message: Message, state: FSMContext):
    """
    Обработка стейта DELETE_CONTACT
    """
    text_handler.delete_line(message.text, message.chat.username)
    await message.answer(
        text=BotTextEnum.AFTER_SUCCESS_DELETE,
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )
    await state.set_state(UserState.CHOOSE_NEXT_OPERATION)
