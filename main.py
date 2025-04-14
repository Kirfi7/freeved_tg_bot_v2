import asyncio
import config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# from filters.filters import IsNotBannedCB, IsNotBannedMSG
# from handlers import (
#     bot_messager,
#     admin_panel,
#     main_dialog,
#     comment_tracker,
# )


async def main():
    bot = Bot(token=config.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    # dp.include_routers(
    #     comment_tracker.router,
    #     admin_panel.router,
    #     main_dialog.router,
    #     bot_messager.router,
    # )

    # dp.message.filter(IsNotBannedMSG())
    # dp.callback_query.filter(IsNotBannedCB())

    print("Бот запущен успешно!")
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
