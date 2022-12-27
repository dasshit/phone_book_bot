import asyncio
import os

from aiogram import Bot, Dispatcher

from project.routers import router


async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()

    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
