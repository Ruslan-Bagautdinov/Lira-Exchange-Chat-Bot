from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv

SERVER = getenv('SERVER', False)

if SERVER:
    TOKEN = getenv('TOKEN')
    URI_APP = getenv('URI_APP')
    ADMIN_ID = getenv('ADMIN_ID')
    HEROKU_APP_NAME = getenv('HEROKU_APP_NAME')
    HEROKU_APP_TOKEN = getenv('HEROKU_APP_TOKEN')
    ADMIN_LINK = getenv('ADMIN_LINK')
    BOT_LINK = getenv('BOT_LINK')
    KURS_ALANYA = getenv('KURS_ALANYA')
    KURS_ANTALYA = getenv('KURS_ANTALYA')
else:
    from config import *
    TOKEN = TOKEN
    URI_APP = URI_APP
    ADMIN_ID = ADMIN_ID
    HEROKU_APP_NAME = HEROKU_APP_NAME
    HEROKU_APP_TOKEN = HEROKU_APP_TOKEN
    ADMIN_LINK = ADMIN_LINK
    BOT_LINK = BOT_LINK
    KURS_ALANYA = KURS_ALANYA
    KURS_ANTALYA = KURS_ANTALYA

storage = MemoryStorage()
bot = Bot(
          token=TOKEN
         )
dp = Dispatcher(bot, storage=storage)
