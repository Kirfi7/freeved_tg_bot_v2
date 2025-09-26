from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery, BotCommandScopeChat
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllChatAdministrators
import config


class MessangerRequest(BaseFilter):
    async def __call__(self, message: Message):
        try:
            text = message.text

            if text.startswith("/start"):
                data = text.split()[1]
                user = data.split('_')[1]

                await self.setup_bot_commands(message)

                return {"target_tg_id": int(user)}
            return False
        except: return False

    @staticmethod
    async def setup_bot_commands(message: Message):
        bot = message.bot
        chat_id = message.chat.id
        user_id = message.from_user.id

        # ЛИЧКА
        if message.chat.type == ChatType.PRIVATE:
            if user_id == config.ADMIN:
                # Персональные команды для админа в его личке
                await bot.set_my_commands(
                    commands=[
                        BotCommand(command="ban", description="Забанить"),
                        BotCommand(command="unban", description="Разбанить"),
                        BotCommand(command="start", description="Старт"),
                    ],
                    scope=BotCommandScopeChat(chat_id=chat_id)
                )
            else:
                await bot.set_my_commands(
                    commands=[
                        BotCommand(command="start", description="Старт"),
                    ],
                    scope=BotCommandScopeChat(chat_id=chat_id)
                )


class MessangerAccepted(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        unpacked_callback = callback.data.split(':')

        if unpacked_callback[0] == "confirmed_contact":
            return {"target_tg_id": int(unpacked_callback[1])}
        return False
