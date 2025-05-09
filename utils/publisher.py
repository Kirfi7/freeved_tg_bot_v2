import config

from aiogram import Bot

from database.models import PostInit

bot = Bot(config.TOKEN)


async def publish(post_data: PostInit):

    if post_data.attachment is None:
        await bot.send_message(
            chat_id=config.CHANNEL,
            text=...,
        )

    elif post_data.attachment.file_type == "document":
        await bot.send_document(
            chat_id=config.CHANNEL,
            document=post_data.attachment.file_id,
            caption=...,
        )

    else:
        await bot.send_photo(
            chat_id=config.CHANNEL,
            photo=post_data.attachment.file_id,
            caption=...,
        )


async def create_text(post_data: PostInit):
    text = (f''
            f''
            f''
            f'')
    return text.strip()