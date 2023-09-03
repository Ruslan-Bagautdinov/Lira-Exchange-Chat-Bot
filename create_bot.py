from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv, environ

SERVER = environ.get('SERVER', False)

if SERVER:
    TOKEN = environ.get('TOKEN')
    ADMIN_ID = environ.get('ADMIN_ID')
else:
    from config import *
    TOKEN = TOKEN
    ADMIN_ID = ADMIN_ID

storage = MemoryStorage()
bot = Bot(
          token=TOKEN
         )
dp = Dispatcher(bot, storage=storage)
