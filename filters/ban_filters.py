from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from database.services.users import UsersDB


class CBFilter(Filter):
    async def __call__(self, callback: CallbackQuery):
        if UsersDB.is_banned(callback.message.from_user.id):
            return False
        return True


class MSGFilter(Filter):
    async def __call__(self, message: Message):
        if UsersDB.is_banned(message.from_user.id):
            return False
        return True