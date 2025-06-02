from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.models import PostInit, PostAttachment
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
    await state.set_data({"pub_type": pub_type})
    await callback.message.edit_text(answer, reply_markup=None)


@router.message(StateFilter(Publication.text))
async def handle_publication_text(message: Message, state: FSMContext):
    fsm_data = await state.get_data()

    if message.content_type == "document":
        attachment = PostAttachment(
            file_type="document",
            file_id=message.document.file_id
        )
        message_text = message.caption
    elif message.content_type == "photo":
        attachment = PostAttachment(
            file_type="photo",
            file_id=message.document.file_id
        )
        message_text = message.caption
    elif message.content_type == "text":
        attachment = None
        message_text = message.text
    else:
        await message.answer("Можно отправить только текст, фото или документ!")
        return

    post_data = PostInit(
        author_id=message.from_user.id,
        author_username=message.from_user.username,
        post_type=fsm_data.get("pub_type"),
        post_text=message_text,
        attachment=attachment,
    )
    print(PostsDB.init_post(post_data))
    pub_count = UsersDB.get_messages_count(message.from_user.id)
    print(pub_count)
    # post_final_data = PostsDB.get_post()
    # Проверить кол-во публикаций пользователя
    # Отправить админу, либо в канал
