from aiogram.exceptions import TelegramForbiddenError

import config

from aiogram import Bot

from database.services.posts import PostsDB

bot = Bot(config.TOKEN)


class Notifier:
    def __init__(self, post_id: int):
        self.post_id = post_id

    async def notify(self, comment_author_id: int, link: str):
        subscribers = set(PostsDB.get_post_subs(self.post_id))
        if comment_author_id in subscribers:
            subscribers.remove(comment_author_id)
        else:
            PostsDB.add_post_sub(self.post_id, comment_author_id)

        for subscriber in subscribers:
            try:
                await bot.send_message(subscriber, link)
            except TelegramForbiddenError:
                pass