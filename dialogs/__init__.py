from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from markups import get_menu_markup
from .admin_conversation import router as admin_conversation
from .channel_posting import router as channel_posting
from .admin_choices import router as admin_choices

base_router = Router()


@base_router.message(CommandStart())
async def start_bot(message: Message):
    markup = await get_menu_markup()
    await message.answer(text="Выберите действие:", reply_markup=markup)


base_router.include_router(channel_posting)
base_router.include_router(admin_choices)
base_router.include_router(admin_conversation)
