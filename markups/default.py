from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_menu_markup() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Помогите советом", callback_data="publication")],
        [InlineKeyboardButton(text="Обратите внимание", callback_data="conversation")],
        [InlineKeyboardButton(text="Обратите внимание", url="https://t.me/notifyparty")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)