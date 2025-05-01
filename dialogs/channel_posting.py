from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.services.users import UsersDB
from database.services.posts import PostsDB

from markups import get_choice_markup


class Publication(StatesGroup):
    text = State()


router = Router()


@router.callback_query(F.callback_data == "publication")
async def start_publication(callback: CallbackQuery):
    markup = await get_choice_markup()
    await callback.message.edit_text("Выберите тип публикации:", reply_markup=markup)


@router.callback_query(F.callback_data.startswith("type"))
async def handle_publication_type(callback: CallbackQuery, state: FSMContext):
    pub_type: str = callback.data.split(":")[1]
    answer = f"Выбранный тип публикации: «{pub_type}»\n"
    answer += "Введите текст сообщения (можно прикрепить 1 файл или 1 фото)."
    await state.set_state(Publication.text)
    await state.set_data({pub_type: pub_type})
    await callback.message.edit_text(answer, reply_markup=None)


@router.message(StateFilter(Publication.text))
async def handle_publication_text(callback: CallbackQuery, state: FSMContext):
    ...