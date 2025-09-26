from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from pydantic.v1.class_validators import all_kwargs

from database.models import PostInit, PostAttachment
from database.services.users import UsersDB
from database.services.posts import PostsDB

from markups import get_choice_markup
from utils.link import get_link
from utils.notifier import Notifier
from utils.publisher import Publisher

import config


class Publication(StatesGroup):
    text = State()


router = Router()


@router.callback_query(F.data == "publication")
async def start_publication(callback: CallbackQuery):
    markup = await get_choice_markup()
    await callback.message.edit_text("Выберите тип публикации:", reply_markup=markup)


@router.callback_query(F.data.startswith("type"))
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
    await state.clear()

    if message.content_type == "document":
        attachment = PostAttachment(
            file_type="document",
            file_id=message.document.file_id
        )
        message_text = message.caption
    elif message.content_type == "photo":
        attachment = PostAttachment(
            file_type="photo",
            file_id=message.photo[-1].file_id
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
        comment_subscribers=[message.from_user.id,],
    )
    post_id = PostsDB.init_post(post_data)
    pub_count = UsersDB.get_messages_count(message.from_user.id)
    is_banned = UsersDB.is_banned(message.from_user.id)
    print("pub_count", pub_count)

    # Проверка лимита
    recent_count = PostsDB.count_last_24h(message.from_user.id)
    if recent_count >= 3:
        return await message.answer('Можно опубликовать не более 3 постов за последние 24 часа.')

    publisher = Publisher(post_id)

    # выбор
    if is_banned:
        return await message.answer('Вы были заблокированы. Обратитесь к Администратору: @kirfi777.')
    elif pub_count > 2:
        msg_id = await publisher.to_prod()
        return await message.answer(f'Ваш пост успешно опубликован!\nСсылка на пост: {get_link(msg_id)}')
    else:
        await publisher.to_admin()
        return await message.answer('Ваш пост отправлен на модерацию. Ожидайте подтверждения.')


@router.message(F.chat.id == config.GROUP)
async def get_comment_object(message: Message):
    if message.reply_to_message:
        post_id = message.reply_to_message.forward_from_message_id

        post_object = PostsDB.get_post_by_tg(post_id)

        notifier = Notifier(post_object.get("id"))
        await notifier.notify(message.from_user.id, get_link(post_id))
    else:
        pass