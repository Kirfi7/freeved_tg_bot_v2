from aiogram import F, Router
from aiogram.types import CallbackQuery

...

router = Router()


@router.callback_query(F.callback_data == "k")
async def init_conversation(callback: CallbackQuery):
    ...