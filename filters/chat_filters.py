from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class MessangerRequest(BaseFilter):
    async def __call__(self, message: Message):
        try:
            text = message.text

            if text.startswith("/start"):
                data = text.split()[1]
                user = data.split('_')[1]

                return {"target_tg_id": int(user)}
            return False
        except: return False


class MessangerAccepted(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        unpacked_callback = callback.data.split(':')

        if unpacked_callback[0] == "confirmed_contact":
            return {"target_tg_id": int(unpacked_callback[1])}
        return False
