from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from keyboards.admin_kb import *


from create_bot import dp, bot, ADMIN_ID
from database import rate_db


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
                config_var_name = 'ALANYA'
            else:
                config_var_name = 'ANTALYA'

            kurs_now = f'Сейчас курс для города {msg.text} - {rate_db.read_rate(config_var_name)}\n'
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

            try:
                rate_db.change_rate(kurs_data["Город"], value)
                await bot.send_message(msg.from_user.id,
                                       f'Для города {kurs_data["Город"]} установлен новый курс',
                                       reply_markup=admin_keyboard
                                       )
                await FSMAdmin.start_edit.set()
            except:
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
