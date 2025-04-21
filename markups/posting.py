from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_choice_markup() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Помогите советом", callback_data="type:Помогите советом")],
        [InlineKeyboardButton(text="Обратите внимание", callback_data="type:Обратите внимание")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_approve_markup(post_id: int, user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Опубликовать", callback_data=f"publish:{post_id}")],
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete:{post_id}")],
        [InlineKeyboardButton(text="Удалить и заблокировать", callback_data=f"ban:{post_id}:{user_id}")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)