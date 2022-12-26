import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from project.handlers import router


async def main():
    logging.basicConfig(level=logging.DEBUG)
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()

    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
