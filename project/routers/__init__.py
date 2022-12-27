from typing import Callable, Any, Awaitable

from aiogram import Router, BaseMiddleware
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.handlers import ErrorHandler
from aiogram.types import Message

from project.db.models import User
from project.misc.enums import UserTextCommandsEnum, BotTextEnum
from project.misc.keyboards import CHOOSE_OPERATION_KEYBOARD
from project.misc.logger import logger
from project.routers import add, show, delete, dump
from project.fsm.state import UserState


class LoggerMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        logger.info(
            f'user: {event.chat.username}, '
            f'state: {await data["state"].get_state()}, '
            f'text: {event.text}, '
            f'contact: {event.contact}'
        )
        return await handler(event, data)


router = Router()
router.message.middleware(LoggerMiddleware())
router.include_router(add.router)
router.include_router(show.router)
router.include_router(delete.router)
router.include_router(dump.router)


@router.errors()
class RouterErrorHandler(ErrorHandler):
    async def handle(self):
        """
        Обработчик ошибок в хэндлерах бота
        """
        logger.exception(self.event.exception)
        await self.bot.send_message(
            chat_id=self.event.update.message.chat.id,
            text=BotTextEnum.ERROR_TEXT.format(self.event.exception),
            reply_to_message_id=self.event.update.message.message_id,
            reply_markup=CHOOSE_OPERATION_KEYBOARD
        )
        await self.data['state'].set_state(UserState.INITIAL_STATE)


@router.message(Command('start'))
async def command_start(message: Message, state: FSMContext):
    """
    Обработка комманды '/start'
    """
    logger.info('Команда /start')
    user_model, _ = User.get_or_create(
        user_name=message.chat.username,
        first_name=message.chat.first_name,
        last_name=message.chat.last_name
    )
    await state.update_data(USER_DB_ID=user_model.id)
    await message.answer(
        text=BotTextEnum.WELCOME_TEXT,
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )
    await state.set_state(UserState.INITIAL_STATE)


@router.message(
    Text(text=UserTextCommandsEnum.BACK.value)
)
async def comming_back(message: Message, state: FSMContext):
    """
    Обработка комманды 'Назад'
    """
    logger.info(f'Возвращаемся из {await state.get_state()} в UserState.INITIAL_STATE')
    await message.answer(
        text=BotTextEnum.COMMIN_BACK,
        reply_markup=CHOOSE_OPERATION_KEYBOARD
    )
    await state.set_state(UserState.INITIAL_STATE)
