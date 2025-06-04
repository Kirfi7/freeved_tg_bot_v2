import config

from aiogram import Bot
from aiogram.types import Message

from database.models import Post
from markups import get_approve_markup

bot = Bot(config.TOKEN)

async def publish(post_data: Post, count: int):
    send_text = await create_text(post_data, count)
    msg: Message

    if count > 2:
        target_chat_id = config.CHANNEL
        markup = None

    else:
        target_chat_id = config.ADMIN
        markup = await get_approve_markup(post_data.id, post_data.author_id)

    if post_data.attachment is None:
        msg = await bot.send_message(
            chat_id=target_chat_id,
            text=send_text,
            reply_markup=markup
        )

    elif post_data.attachment.file_type == "document":
        msg = await bot.send_document(
            chat_id=target_chat_id,
            document=post_data.attachment.file_id,
            caption=send_text,
            reply_markup=markup
        )

    else:
        msg = await bot.send_photo(
            chat_id=target_chat_id,
            photo=post_data.attachment.file_id,
            caption=send_text,
            reply_markup=markup
        )

    return msg.message_id  # Возвращаем id опубликованного поста


async def create_text(post_data: Post, count: int):
    text = (f'Номер сообщения: {post_data.id}'
            f'Вид сообщения: {post_data.post_type}'
            f'Кол-во сообщений пользователя: {count}'
            f'Идентификатор пользователя: {post_data.author_id}'
            f'Имя пользователя: {post_data.author_username or "Нет"}'
            f'Текст сообщения:\n\n{post_data.post_text}')
    return text.strip()