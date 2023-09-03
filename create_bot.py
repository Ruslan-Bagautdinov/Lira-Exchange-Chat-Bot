from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv

TOKEN = getenv('TOKEN')
ADMIN_ID = getenv('ADMIN_ID')
KURS_ALANYA = getenv('KURS_ALANYA')
KURS_ANTALYA = getenv('KURS_ANTALYA')


storage = MemoryStorage()
bot = Bot(
          token=TOKEN
         )
dp = Dispatcher(bot, storage=storage)
