from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ForceReply

import config
from database.services.users import UsersDB

router = Router()

class AdminFSM(StatesGroup):
    waiting_ban_id = State()
    waiting_unban_id = State()

def _is_admin(uid: int) -> bool:
    return int(uid) == int(config.ADMIN)


@router.callback_query(F.data == "user_ban")
async def cb_ban(cb: CallbackQuery, state: FSMContext):
    if not _is_admin(cb.from_user.id):
        return await cb.answer("Нет прав", show_alert=True)
    await state.set_state(AdminFSM.waiting_ban_id)
    await cb.message.answer("Введите telegram_id для блокировки:", reply_markup=ForceReply())
    await cb.answer()


@router.callback_query(F.data == "user_unban")
async def cb_unban(cb: CallbackQuery, state: FSMContext):
    if not _is_admin(cb.from_user.id):
        return await cb.answer("Нет прав", show_alert=True)
    await state.set_state(AdminFSM.waiting_unban_id)
    await cb.message.answer("Введите telegram_id для разблокировки:", reply_markup=ForceReply())
    await cb.answer()


@router.message(AdminFSM.waiting_ban_id)
async def fsm_ban(msg: Message, state: FSMContext):
    if not _is_admin(msg.from_user.id):
        return await msg.answer("Нет прав.")
    if not msg.text.isdigit():
        return await msg.answer("Введите числовой telegram_id.")
    telegram_id = int(msg.text)
    if not UsersDB.get_user(telegram_id):
        await state.clear()
        return await msg.answer(f"Пользователь {telegram_id} не найден.")
    UsersDB.ban_user(telegram_id)
    await msg.answer(f"Пользователь {telegram_id} заблокирован ✅")
    await state.clear()


@router.message(AdminFSM.waiting_unban_id)
async def fsm_unban(msg: Message, state: FSMContext):
    if not _is_admin(msg.from_user.id):
        return await msg.answer("Нет прав.")
    if not msg.text.isdigit():
        return await msg.answer("Введите числовой telegram_id.")
    telegram_id = int(msg.text)
    if not UsersDB.get_user(telegram_id):
        await state.clear()
        return await msg.answer(f"Пользователь {telegram_id} не найден.")
    UsersDB.unban_user(telegram_id)
    await msg.answer(f"Пользователь {telegram_id} разблокирован ✅")
    await state.clear()
