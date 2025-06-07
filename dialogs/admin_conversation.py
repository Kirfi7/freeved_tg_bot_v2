from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

router = Router()


@router.callback_query(F.callback_data == "conversation")
async def init_conversation(callback: CallbackQuery):
    ...


@router.message()
async def handle_message(message: Message):
    ...


@router.callback_query()
async def reply_to_message(callback: CallbackQuery):
    ...


@router.message()
async def handle_reply(message: Message):
    ...