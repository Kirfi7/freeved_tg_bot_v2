import config

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup

from database.models import Post
from database.services.posts import PostsDB
from database.services.users import UsersDB
from markups import get_approve_markup

bot = Bot(config.TOKEN)


class Publisher:
    def __init__(self, post_id: int):
        self.post_id = post_id

    async def to_admin(self) -> None:
        """
        Сообщение на модерацию
        """
        post = await self.__get_from_db()
        msgs_cnt = await self.__get_messages_count(post.author_id)
        text = await self.__create_text(post, msgs_cnt)

        markup = await get_approve_markup(post.id, post.author_id)
        await self.__publish(config.ADMIN, post, text, markup)

    async def to_prod(self) -> int:
        """
        Публикует сообщение в канал
        """
        post = await self.__get_from_db()
        msgs_cnt = await self.__get_messages_count(post.author_id)
        # Для канала публикуем только текст пользователя без служебной информации
        text = await self.__create_text(post, msgs_cnt + 1, concise=True)

        msg_id = await self.__publish(config.CHANNEL, post, text)
        PostsDB.publish_post(post.id, msg_id)
        return msg_id

    @staticmethod
    async def __get_messages_count(author_id: int) -> int:
        return UsersDB.get_messages_count(author_id)

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
        return PostsDB.get_post(post_id=self.post_id)

    @staticmethod
    async def __create_text(post, count, *, concise: bool = False) -> str:
        if concise:
            header = post.post_type or ""
            body = post.post_text or ""
            # В канал: только тип публикации и сам текст
            return f"{header}\n\n{body}"

        text = (f'Номер сообщения: {post.id}\n'
                f'Вид сообщения: {post.post_type}\n'
                f'Кол-во сообщений пользователя: {count}\n'
                f'Идентификатор пользователя: {post.author_id}\n'
                f'Имя пользователя: {post.author_username or "Нет"}\n\n'
                f'Текст сообщения:\n{post.post_text}')
        return text.strip()
