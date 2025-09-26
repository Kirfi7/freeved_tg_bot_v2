from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config


async def get_menu_markup(message: Message) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Написать сообщение в канал", callback_data="publication")],
        [InlineKeyboardButton(text="Связаться с администратором", callback_data="conversation")],
        [InlineKeyboardButton(text="Заказать логистическую услугу", url="https://t.me/notifyparty")],
    ]

    if message.from_user.id == config.ADMIN:
        buttons += [
            [InlineKeyboardButton(text="Заблокировать пользователя", callback_data="ban")],
            [InlineKeyboardButton(text="Разблокировать пользователя", callback_data="unban")]
        ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)