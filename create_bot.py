from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import environ

TOKEN = environ.get('TOKEN')
ADMIN_ID = environ.get('ADMIN_ID')
KURS_ALANYA = environ.get('KURS_ALANYA')
KURS_ANTALYA = environ.get('KURS_ANTALYA')


storage = MemoryStorage()
bot = Bot(
          token=TOKEN
         )
dp = Dispatcher(bot, storage=storage)
