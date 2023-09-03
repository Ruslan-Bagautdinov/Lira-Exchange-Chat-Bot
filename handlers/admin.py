from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from keyboards.admin_kb import *

import os
import shutil
from os import getenv

from create_bot import dp, bot, ADMIN_ID


ADMIN_USER_ID = int(ADMIN_ID)
# ID = None


class FSMAdmin(StatesGroup):

    start_edit = State()
    ready_to_edit = State()


async def admin_check(msg: types.Message):

    if msg.from_user.id == ADMIN_USER_ID:

        await bot.send_message(msg.from_user.id,
                               "Доступ разрешен",
                               reply_markup=admin_keyboard
                               )
        await FSMAdmin.start_edit.set()

    else:

        await bot.delete_message(msg.chat.id, msg.message_id)


async def starting_edit(msg: types.Message, state: FSMContext):

    if msg.from_user.id == ADMIN_USER_ID:
        if msg.text == CANCEL_ADMIN:
            await bot.send_message(msg.from_user.id,
                                   "До свидания!",
                                   reply_markup=ReplyKeyboardRemove())
            await state.finish()
        else:
            await FSMAdmin.ready_to_edit.set()
            async with state.proxy() as kurs_data:
                kurs_data["Город"] = msg.text
            if msg.text == 'Алания':
                config_var_name = 'KURS_ALANYA'
            else:
                config_var_name = 'KURS_ANTALYA'

            kurs_now = f'Сейчас курс для города {msg.text} - {getenv(config_var_name)}\n'
            await bot.send_message(msg.from_user.id,
                                   kurs_now)

            answer = f'Введите курс для города {msg.text}\n'
            await bot.send_message(msg.from_user.id,
                                   answer,
                                   reply_markup=ReplyKeyboardRemove())


async def entering_value(msg: types.Message, state: FSMContext):

    try:
        value = msg.text.replace(',', '.')
        value = round(float(value), 2)

        async with state.proxy() as kurs_data:

            answer = change_the_kurs(kurs_data["Город"], value)

            if answer:
                await bot.send_message(msg.from_user.id,
                                       f'Для города {kurs_data["Город"]} установлен новый курс',
                                       reply_markup=admin_keyboard
                                       )
                await FSMAdmin.start_edit.set()
            else:
                await bot.send_message(msg.from_user.id,
                                       'Неизвестная ошибка',
                                       reply_markup=admin_keyboard
                                       )
                await FSMAdmin.start_edit.set()

    except ValueError:
        await bot.send_message(msg.from_user.id,
                               'Число не распознано...',
                               reply_markup=admin_keyboard
                               )
        await FSMAdmin.start_edit.set()


def change_the_kurs(city, value, answer=False):

    path = os.path.join('/etc', 'environment')
    if city == 'Алания':
        config_var_name = 'KURS_ALANYA'
    else:
        config_var_name = 'KURS_ANTALYA'

    with open(path, 'r') as file:
        lines = file.readlines()

    shutil.copyfile(path, path + '.bak')

    with open(path, 'w') as file:
        for line in lines:
            if line.startswith(config_var_name + '='):
                line = line.replace(line, f'{config_var_name}={value}\n')
                answer = True
            file.write(line)
    return answer


def register_handlers_admin(dp: Dispatcher):

    dp.register_message_handler(admin_check,
                                Text(equals='Курс'),
                                state=None
                                )

    dp.register_message_handler(starting_edit,
                                Text(equals=KURS_ANTALYA_ADMIN),
                                state=FSMAdmin.start_edit
                                )

    dp.register_message_handler(starting_edit,
                                Text(equals=KURS_ALANYA_ADMIN),
                                state=FSMAdmin.start_edit
                                )

    dp.register_message_handler(starting_edit,
                                Text(equals=CANCEL_ADMIN),
                                state=FSMAdmin.start_edit
                                )

    dp.register_message_handler(entering_value,
                                content_types=["text"],
                                state=FSMAdmin.ready_to_edit
                                )
