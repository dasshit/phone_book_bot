from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from project.misc.enums import UserTextCommandsEnum, BotTextEnum
from project.misc.keyboards import SHOW_CONTACT_KEYBOARD
from project.routers.show import show_line, show_vcard
from project.fsm.state import UserState

from project.routers.show import show_vcard, show_line

router = Router()
router.include_router(show_vcard.router)
router.include_router(show_line.router)


@router.message(
    UserState.INITIAL_STATE,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT.value)
)
async def choose_write_contact(message: Message, state: FSMContext):
    """
    Обработка комманды 'Записать контакт'
    """
    await message.reply(
        text=BotTextEnum.ENTER_CONTACT,
        reply_markup=SHOW_CONTACT_KEYBOARD
    )
    await state.set_state(UserState.SHOW_CONTACT)
