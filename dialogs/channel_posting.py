from aiogram import F, Router
from aiogram.types import CallbackQuery

from markups import get_choice_markup

router = Router()


@router.callback_query(F.callback_data == "publication")
async def start_publication(callback: CallbackQuery):
    markup = await get_choice_markup()
    await callback.message.edit_text("Выберите тип публикации:", reply_markup=markup)


@router.callback_query(F.callback_data.startswith("type"))
async def handle_publication_type(callback: CallbackQuery):
    ...