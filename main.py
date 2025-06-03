import sys
import asyncio
import logging
import config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dialogs import base_router


async def main():
    bot = Bot(token=config.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    dp.include_router(base_router)

    # dp.message.filter(IsNotBannedMSG())
    # dp.callback_query.filter(IsNotBannedCB())

    print("Бот запущен успешно!")
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
