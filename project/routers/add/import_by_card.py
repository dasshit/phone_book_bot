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
    Text(text=UserTextCommandsEnum.WRITE_CONTACT_BY_CARD.value)
)
async def contact_by_card(message: Message, state: FSMContext):
    """
    Импорт контакта через контакт из адресной книги телефона
    """
    await message.reply(
        text="Загрузите карточку контакта",
        reply_markup=BACK_KEYBOARD,
    )
    await state.set_state(UserState.IMPORT_CONTACT_BY_CARD)


@router.message(
    UserState.IMPORT_CONTACT_BY_CARD
)
async def import_contact_by_card(message: Message, state: FSMContext):
    """
    Импорт контакта через контакт из адресной книги телефона
    """
    if message.contact is None:
        await message.reply(
            text='Пришлите карточку контакта!'
        )

    Contact.create(
        user=get_user_model(state),
        first_name=message.contact.first_name,
        last_name=message.contact.last_name,
        phone=message.contact.phone_number,
        contact_type='VCARD'
    )

    await message.reply(
        text=BotTextEnum.ADD_CONTACT_SUCCESS,
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )
    await state.set_state(UserState.INITIAL_STATE)
