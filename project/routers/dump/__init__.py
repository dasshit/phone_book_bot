import time

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from project.fsm.state import UserState
from project.misc.enums import UserTextCommandsEnum
from project.misc.logger import logger
from project.db.models import Contact, User
from project.misc.utils import get_user_model, writeToCsv

router = Router()


@router.message(
    UserState.INITIAL_STATE,
    Text(text=UserTextCommandsEnum.SHOW_CONTACT_FILE.value)
)
async def dump_book(message: Message, state: FSMContext):
    logger.info('Получаем адресную книгу')

    contact_tuples = Contact.select().where(Contact.user == await get_user_model(state)).tuples()

    contacts_file = "my_contacts_{}.csv".format(time.time_ns())

    writeToCsv(contact_tuples, contacts_file)

    await message.reply_document(FSInputFile(contacts_file))
