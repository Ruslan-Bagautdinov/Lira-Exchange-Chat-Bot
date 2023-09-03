from aiogram.utils import executor
from aiogram.types import BotCommand

from os import getenv


from create_bot import dp, bot, URI_APP, SERVER
from handlers import client, admin


async def on_startup(dp):

    admin.register_handlers_admin(dp)
    client.register_handlers_client(dp)

    if SERVER:
        await bot.set_webhook(URI_APP)

    commands = [
        BotCommand(command="/start", description=chr(0x1F44B) + " СТАРТ")
    ]

    await bot.set_my_commands(commands)


async def on_shutdown(dp):

    if SERVER:
        await bot.delete_webhook()
    pass


if SERVER:

    PORT = getenv('PORT', '8443')

    executor.start_webhook(
                           dispatcher=dp,
                           webhook_path='',
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True,
                           host="0.0.0.0",
                           port=PORT
                           )
else:

    executor.start_polling(
                           dispatcher=dp,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True
                           )
