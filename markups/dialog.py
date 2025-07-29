from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def contact_with_user_button(user_tg_id: int):
    buttons = [
        [InlineKeyboardButton(
            text="Написать сообщение через бота",
            callback_data=F"confirmed_contact:{user_tg_id}",
        )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
