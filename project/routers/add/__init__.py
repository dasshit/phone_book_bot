from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from project.misc.enums import UserTextCommandsEnum, BotTextEnum
from project.misc.keyboards import ENTER_CONTACT_KEYBOARD
from project.routers.add import import_by_card, import_by_step
from project.fsm.state import UserState

router = Router()
router.include_router(import_by_card.router)
router.include_router(import_by_step.router)


@router.message(
    UserState.INITIAL_STATE,
    Text(text=UserTextCommandsEnum.WRITE_CONTACT.value)
)
async def choose_write_contact(message: Message, state: FSMContext):
    """
    Обработка комманды 'Записать контакт'
    """
    await message.reply(
        text=BotTextEnum.ENTER_CONTACT,
        reply_markup=ENTER_CONTACT_KEYBOARD
    )
    await state.set_state(UserState.IMPORT_CONTACT_START)
