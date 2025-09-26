from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.services.posts import PostsDB
from database.services.users import UsersDB
from utils.publisher import Publisher, bot

router = Router()


@router.callback_query(F.data.startswith("publish"))
async def publish(call: CallbackQuery):
    await call.message.delete_reply_markup()
    _, post_id = call.data.split(":")
    post_id = int(post_id)
    author_id = PostsDB.get_post(post_id).author_id

    publisher = Publisher(post_id)
    await publisher.to_prod()

    await call.message.reply("Сообщение успешно отправлено!")
    await call.bot.send_message(author_id, "Ваш пост был опубликован!")


@router.callback_query(F.data.startswith("delete"))
async def cancel(call: CallbackQuery):
    await call.message.delete_reply_markup()
    _, post_id = call.data.split(":")
    post_id = int(post_id)
    author_id = PostsDB.get_post(post_id).author_id

    PostsDB.del_post(post_id)

    await call.message.reply("Сообщение успешно удалено!")
    await call.bot.send_message(author_id, "Ваш пост не прошёл модерацию.")


@router.callback_query(F.data.startswith("ban"))
async def ban(call: CallbackQuery):
    await call.message.delete_reply_markup()
    _, post_id, user_id = call.data.split(":")
    PostsDB.del_post(int(post_id))
    UsersDB.ban_user(int(user_id))
    await call.message.reply("Сообщение успешно удалено! Пользователь заблокирован.")