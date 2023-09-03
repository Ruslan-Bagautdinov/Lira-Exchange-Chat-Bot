from aiogram.utils import executor
from aiogram.types import BotCommand

from create_bot import dp, bot
from handlers import client, admin
from database import rate_db


async def on_startup(dp):

    rate_db.sql_start()
    admin.register_handlers_admin(dp)
    client.register_handlers_client(dp)

    commands = [
        BotCommand(command="/start", description=chr(0x1F44B) + " СТАРТ")
    ]

    await bot.set_my_commands(commands)


executor.start_polling(
                       dispatcher=dp,
                       on_startup=on_startup,
                       skip_updates=True
                       )
