from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from project.db.models import Contact
from project.fsm.state import UserState
from project.misc.enums import UserTextCommandsEnum, BotTextEnum
from project.misc.keyboards import BACK_KEYBOARD, CHOOSE_OPERATION_KEYBOARD
from project.misc.utils import get_user_model

router = Router()


@router.message(
    UserState.SHOW_CONTACT,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT_MULTI_LINE.value)
)
async def choose_show_contact(message: Message, state: FSMContext):
    """
    Обработка комманды 'Записать контакт'
    """
    await message.reply(
        text=BotTextEnum.ENTER_CONTACT_DATA,
        reply_markup=BACK_KEYBOARD
    )
    await state.set_state(UserState.SHOW_CONTACT_MULTILINE)


@router.message(
    UserState.SHOW_CONTACT_MULTILINE
)
async def show_contact_multiline(message: Message, state: FSMContext):
    """
    Отображение всех найденных контактов текстом
    """
    text = message.text.strip()

    contact_query = Contact.select().where(
        Contact.user == get_user_model(state),
        (Contact.first_name == text) | (Contact.last_name == text) | (Contact.phone == text)
    )

    assert contact_query.count(), BotTextEnum.CONTACT_NOT_FOUND

    for cnt_model in contact_query:
        await message.answer(
            text=BotTextEnum.MULTI_LINE_CONTACT.format(
                cnt_model.last_name,
                cnt_model.first_name,
                cnt_model.phone,
                cnt_model.contact_type,
            ),
            reply_markup=CHOOSE_OPERATION_KEYBOARD
        )
    await state.set_state(UserState.INITIAL_STATE)
