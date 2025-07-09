from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message, CallbackQuery

from database.models import User
from database.services.users import UsersDB

import config

bot = Bot(config.TOKEN)


class UsersMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ):
        user_id: int = data.get("event_from_user").id
        user = UsersDB.get_user(user_id)

        if user is None:
            UsersDB.add_user(User(telegram_id=user_id))

        elif user.get('is_banned'):
            await bot.send_message(user_id, "Вы заблокированы! Любые действия с ботом невозможны.")
            return None

        result = await handler(event, data)
        return result
