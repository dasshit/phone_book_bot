from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from project.db.models import Contact
from project.fsm.state import UserState
from project.misc.enums import BotTextEnum, UserTextCommandsEnum
from project.misc.keyboards import BACK_KEYBOARD, CHOOSE_OPERATION_KEYBOARD
from project.misc.utils import get_user_model

router = Router()


@router.message(
    UserState.IMPORT_CONTACT_START,
    Text(text=UserTextCommandsEnum.WRITE_CONTACT_BY_PARTS.value)
)
async def contact_by_card(message: Message, state: FSMContext):
    """
    Импорт контакта через контакт из адресной книги телефона
    """
    await message.reply(
        text="Введите фамилию контакта",
        reply_markup=BACK_KEYBOARD,
    )
    await state.set_state(UserState.ENTER_LAST_NAME)


@router.message(
    UserState.ENTER_LAST_NAME
)
async def enter_last_name(message: Message, state: FSMContext):
    """
    Ввод фамилии контакта
    """
    if message.text is None:
        await message.reply(
            text='Введите фамилию текстом'
        )
    await state.update_data(LAST_NAME=message.text.strip())
    await message.reply(
        text="Отлично, теперь введите имя контакта"
    )
    await state.set_state(UserState.ENTER_FIRST_NAME)


@router.message(
    UserState.ENTER_FIRST_NAME
)
async def enter_first_name(message: Message, state: FSMContext):
    """
    Ввод имени контакта
    """
    if message.text is None:
        await message.reply(
            text='Введите имя текстом'
        )
    await state.update_data(FIRST_NAME=message.text.strip())
    await message.reply(
        text="Отлично, теперь введите номер контакта"
    )
    await state.set_state(UserState.ENTER_PHONE)


@router.message(
    UserState.ENTER_PHONE
)
async def enter_phone(message: Message, state: FSMContext):
    """
    Ввод номера контакта
    """
    if message.text is None:
        await message.reply(
            text='Введите номер текстом'
        )
    await state.update_data(PHONE=message.text.strip())
    await message.reply(
        text="Отлично, теперь введите тип контакта"
    )
    await state.set_state(UserState.ENTER_CONTACT_TYPE)


@router.message(
    UserState.ENTER_CONTACT_TYPE
)
async def enter_last_name(message: Message, state: FSMContext):
    """
    Ввод типа контакта и сохранения его в базу
    """
    if message.text is None:
        await message.reply(
            text='Введите тип текстом'
        )

    Contact.create(
        user=get_user_model(state),
        first_name=data['FIRST_NAME'],
        last_name=data['LAST_NAME'],
        phone=data['PHONE'],
        contact_type=message.text.strip()
    )

    await message.reply(
        text=BotTextEnum.ADD_CONTACT_SUCCESS,
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )
    await state.set_state(UserState.INITIAL_STATE)
