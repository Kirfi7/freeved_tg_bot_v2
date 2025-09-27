from aiogram.types import Message

import config


TELEGRAM = 'https://t.me/'


def get_link(msg_id: int) -> str:
    link = F'{TELEGRAM}/c/{config.LINK_ID}/{msg_id}'
    return link

def _short_chat_id(chat_id: int) -> str:
    s = str(chat_id)
    return s[4:] if s.startswith("-100") else s.lstrip("-")

def build_comment_link(message: Message, *, post_id: int,
                       channel_username: str | None = None) -> str:
    thread_id = getattr(message, "reply_to_top_message_id", None)

    if thread_id is None and message.reply_to_message:
        if getattr(message.reply_to_message, "forward_from_message_id", None):
            thread_id = message.reply_to_message.message_id
        else:
            thread_id = getattr(message.reply_to_message, "reply_to_top_message_id", None)

    if thread_id is None:
        thread_id = message.reply_to_message.message_id if message.reply_to_message else None

    if thread_id is None:
        raise ValueError("Не удалось определить thread_id для ссылки на комментарий")

    comment_id = message.message_id

    if channel_username:
        # публичный канал
        return (
            f"https://t.me/{channel_username}/{post_id}"
            f"?single&thread={thread_id}&comment={comment_id}"
        )

    # приватная дискуссия
    short_id = _short_chat_id(message.chat.id)
    return f"https://t.me/c/{short_id}/{comment_id}?thread={thread_id}"
