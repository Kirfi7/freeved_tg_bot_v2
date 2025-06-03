from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_menu_markup() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Написать сообщение в канал", callback_data="publication")],
        [InlineKeyboardButton(text="Связаться с администратором", callback_data="conversation")],
        [InlineKeyboardButton(text="Заказать логистическую услугу", url="https://t.me/notifyparty")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)