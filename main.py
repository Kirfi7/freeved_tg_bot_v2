import sys
import asyncio
import logging
import config

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

from database.services.users import UsersDB
from dialogs import base_router
from filters.ban_filters import MSGFilter, CBFilter
from mddleware.users_middleware import UsersMiddleware


async def main():
    bot = Bot(token=config.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    dp.include_router(base_router)

    # dp.message.filter(MSGFilter())
    # dp.callback_query.filter(CBFilter())
    dp.update.middleware(UsersMiddleware())

    print("Бот запущен успешно!")
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
