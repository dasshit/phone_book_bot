from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from project.db.models import Contact
from project.fsm.state import UserState
from project.misc.logger import logger
from project.misc.enums import UserTextCommandsEnum, BotTextEnum
from project.misc.keyboards import BACK_KEYBOARD, CHOOSE_OPERATION_KEYBOARD
from project.misc.utils import get_user_model

router = Router()


@router.message(
    UserState.INITIAL_STATE,
    Text(text=UserTextCommandsEnum.DELETE_CONTACT.value)
)
async def choose_delete_contact(message: Message, state: FSMContext):
    """
    Обработка комманды 'Записать контакт'
    """
    logger.info(f'Переход в режим удаления контакта')
    await message.reply(
        text=BotTextEnum.ENTER_NUMBER_TO_DELETE_CONTACT,
        reply_markup=BACK_KEYBOARD
    )
    await state.set_state(UserState.DELETE_CONTACT)


@router.message(UserState.DELETE_CONTACT)
async def delete_contact(message: Message, state: FSMContext):
    """
    Удаление контакта
    """
    logger.info('Поиск и удаление контакта из базы')
    contact_query = Contact.select().where(
        Contact.user == await get_user_model(state),
        Contact.phone == message.text.strip()
    )

    assert contact_query.count(), BotTextEnum.CONTACT_NOT_FOUND

    contact_model = contact_query.get()
    contact_model.delete_instance()

    await message.reply(
        text=BotTextEnum.AFTER_SUCCESS_DELETE,
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )

    await state.set_state(UserState.INITIAL_STATE)
