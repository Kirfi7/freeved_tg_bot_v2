from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramForbiddenError
from aiogram.utils.text_decorations import html_decoration as hd
from aiogram import Bot
import config
from database.services.posts import PostsDB

bot = Bot(config.TOKEN)


class Notifier:
    def __init__(self, post_id: int):
        self.post_id = post_id

    async def notify(self, comment_author_id: int, thread_link: str, comment_link: str):
        subscribers = set(PostsDB.get_post_subs(self.post_id))
        if comment_author_id in subscribers:
            subscribers.remove(comment_author_id)
        else:
            PostsDB.add_post_sub(self.post_id, comment_author_id)

        text = (
            f'Под {hd.link(thread_link, "постом")} оставили новый комментарий.\n{hd.link(comment_link, "Открыть")}.'
        )

        for subscriber in subscribers:
            try:
                await bot.send_message(
                    subscriber,
                    text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
            except TelegramForbiddenError:
                pass