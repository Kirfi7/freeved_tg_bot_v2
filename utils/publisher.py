import config

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup

from database.models import Post
from database.services.posts import PostsDB
from markups import get_approve_markup

bot = Bot(config.TOKEN)


class Publisher:
    def __init__(self, post_id: int, msgs_count: int):
        self.msgs_count = msgs_count
        self.post_id = post_id

    async def to_admin(self) -> None:
        """
        Сообщение на модерацию
        """
        post = await self.__get_from_db()
        text = await self.__create_text(post, self.msgs_count)

        markup = await get_approve_markup(post.id, post.author_id)
        await self.__publish(config.ADMIN, post, text, markup)

    async def to_prod(self) -> None:
        """
        Публикует сообщение в канал
        """
        post = await self.__get_from_db()
        text = await self.__create_text(post, self.msgs_count)

        msg_id = await self.__publish(config.CHANNEL, post, text)
        PostsDB.publish_post(post.id, msg_id)

    @staticmethod
    async def __publish(chat_id: int, post: Post, text: str, markup: InlineKeyboardMarkup = None):
        if post.attachment is None:
            msg = await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=markup
            )

        elif post.attachment.file_type == "document":
            msg = await bot.send_document(
                chat_id=chat_id,
                document=post.attachment.file_id,
                caption=text,
                reply_markup=markup
            )

        else:
            msg = await bot.send_photo(
                chat_id=chat_id,
                photo=post.attachment.file_id,
                caption=text,
                reply_markup=markup
            )
        return msg.message_id

    async def __get_from_db(self) -> Post:
        data = PostsDB.get_post(post_id=self.post_id)
        return Post(**data)

    @staticmethod
    async def __create_text(post, count) -> str:
        text = (f'Номер сообщения: {post.id}'
                f'Вид сообщения: {post.post_type}'
                f'Кол-во сообщений пользователя: {count}'
                f'Идентификатор пользователя: {post.author_id}'
                f'Имя пользователя: {post.author_username or "Нет"}'
                f'Текст сообщения:\n\n{post.post_text}')
        return text.strip()