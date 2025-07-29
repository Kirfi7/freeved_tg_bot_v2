import config

from aiogram import Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_filters import MessangerRequest, MessangerAccepted
from markups.dialog import contact_with_user_button

router = Router()
bot = Bot(config.TOKEN, parse_mode='HTML')


class Messanger(StatesGroup):
    message_text = State()


class MsgToAdmin(StatesGroup):
    message_text = State()


@router.message(Command("admin_contact"))
async def admin_contact(message: Message, state: FSMContext):
    await message.answer("Введите текст сообщения для администратора:")
    await state.set_state(MsgToAdmin.message_text)


@router.message(StateFilter(MsgToAdmin.message_text))
async def get_text_to_admin(message: Message, state: FSMContext):
    await bot.send_message(
        chat_id=config.ADMIN,
        text=F"<b>Сообщение от пользователя №{message.from_user.id}:</b>\n\n{message.text}",
        reply_markup=await contact_with_user_button(message.from_user.id),
    )
    await message.reply("Сообщение успешно отправлено!")
    await state.clear()


@router.message(MessangerRequest())
async def contact_with_user_by_call(message: Message, target_tg_id: int):
    markup = await contact_with_user_button(target_tg_id)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=F"Подтвердите, что хотите связаться с пользователем {target_tg_id}",
        reply_markup=markup
    )


@router.callback_query(MessangerAccepted())
async def accepted_contact(callback: CallbackQuery, state: FSMContext, target_tg_id: int):
    await state.set_state(Messanger.message_text)
    await state.update_data({"user_id": target_tg_id})
    who = "администратора" if target_tg_id == config.ADMIN else "пользователя"
    await callback.message.answer(f"Введите текст вашего сообщения для {who}:")
    await callback.answer()


@router.message(StateFilter(Messanger.message_text))
async def get_message_text(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    user_id: int = data['user_id']
    await bot.send_message(
        chat_id=user_id,
        text=F"<b>Сообщение от пользователя №{message.from_user.id}:</b>\n\n{message.text}",
        reply_markup=await contact_with_user_button(message.from_user.id),
    )
    await message.reply("Сообщение успешно отправлено!")
    await state.clear()


@router.callback_query()
async def answer_to_empty_callback(callback: CallbackQuery):
    await callback.answer()