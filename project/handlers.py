import os.path

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.filters.command import Command

from project.enums import BotTextEnum, UserTextCommandsEnum
from project.keyboards import log_in_out_keyboard, logout_keyboard
from project import text_handler


router = Router()


class UserState(StatesGroup):
    choose_operation_type = State()
    delete_contact = State()
    get_file = State()
    log_in_operation = State()
    log_out_operation = State()
    log_out_one_line = State()
    log_out_lines = State()


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

    try:
        assert os.path.exists(
            os.path.join('contacts', f'phone_book_{message.chat.username}.txt')
        ), "Запишите хотя бы один контакт, книга пуста"
        await message.answer(
            text=BotTextEnum.CHOOSE_OUTPUT_FORMAT,
            reply_markup=logout_keyboard
        )
        await state.set_state(UserState.log_out_operation)
    except AssertionError as error:
        await message.answer(
            text=BotTextEnum.ERROR_TEXT.format(error),
            reply_markup=log_in_out_keyboard
        )
        await state.set_state(UserState.choose_operation_type)



@router.message(
    UserState.choose_operation_type,
    Text(text=UserTextCommandsEnum.DELETE_CONTACT.value)
)
async def choose_operation(message: Message, state: FSMContext):
    try:
        assert os.path.exists(
            os.path.join('contacts', f'phone_book_{message.chat.username}.txt')
        ), "Запишите хотя бы один контакт, книга пуста"
        await message.answer(
            text=BotTextEnum.ENTER_NUMBER_TO_DELETE_CONTACT,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(UserState.delete_contact)
    except AssertionError as error:
        await message.answer(
            text=BotTextEnum.ERROR_TEXT.format(error),
            reply_markup=log_in_out_keyboard
        )
        await state.set_state(UserState.choose_operation_type)


@router.message(
    UserState.choose_operation_type,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT_FILE.value)
)
async def choose_operation(message: Message, state: FSMContext):
    try:
        assert os.path.exists(
            os.path.join('contacts', f'phone_book_{message.chat.username}.txt')
        ), "Запишите хотя бы один контакт, книга пуста"
        await message.reply_document(
            FSInputFile(
                os.path.join(
                    'contacts',
                    f'phone_book_{message.chat.username}.txt'
                )))
    except AssertionError as error:
        await message.answer(
            text=BotTextEnum.ERROR_TEXT.format(error),
            reply_markup=log_in_out_keyboard
        )
        await state.set_state(UserState.choose_operation_type)


@router.message(UserState.log_in_operation)
async def log_in_operation(message: Message, state: FSMContext):
    try:
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
    except Exception as error:
        await message.answer(
            text=BotTextEnum.ERROR_TEXT.format(error),
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

    try:

        await message.answer(
            text=', '.join(text_handler.find_line(
                line=message.text,
                user_name=message.chat.username
            )),
            reply_markup=log_in_out_keyboard
        )
        await state.set_state(UserState.choose_operation_type)
    except Exception as error:
        await message.answer(
            text=BotTextEnum.ERROR_TEXT.format(error),
            reply_markup=log_in_out_keyboard
        )
        await state.set_state(UserState.choose_operation_type)


@router.message(UserState.log_out_lines)
async def logging_out_lines(message: Message, state: FSMContext):
    try:
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
    except Exception as error:
        await message.answer(
            text=BotTextEnum.ERROR_TEXT.format(error),
            reply_markup=log_in_out_keyboard
        )
        await state.set_state(UserState.choose_operation_type)


@router.message(UserState.delete_contact)
async def delete_contact(message: Message, state: FSMContext):
    try:
        text_handler.delete_line(message.text, message.chat.username)
        await message.answer(
            text=BotTextEnum.AFTER_SUCCESS_DELETE,
            reply_markup=log_in_out_keyboard
        )
        await state.set_state(UserState.choose_operation_type)
    except Exception as error:
        await message.answer(
            text=BotTextEnum.ERROR_TEXT.format(error),
            reply_markup=log_in_out_keyboard
        )
        await state.set_state(UserState.choose_operation_type)
