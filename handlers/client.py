from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_calendar_rus import simple_cal_callback, SimpleCalendar
from aiogram.types import ReplyKeyboardRemove

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

# own imports

from keyboards import *

from create_bot import dp, bot
from create_bot import ADMIN_ID
from database import rate_db


CHOOSE_DATE_MESSAGE = f'{chr(0x1F4C5)} Выберите дату'

CHOOSE_CITY_MESSAGE = f'{chr(0x1F3D6)} Укажите город\n' \
                      f'Обменный курс в каждом городе свой'

CHOOSE_ADDRESS_MESSAGE = (f'Давайте выберем место встречи с курьером\n'
                          f'Вы можете написать в сообщении\n'
                          f'{chr(0x1F3E0)} Ваш адрес, {chr(0x2708)} аэропорт или\n'
                          f'{chr(0x1F3D6)} название Вашего отеля\n'
                          f'или внизу экрана нажать на кнопку\n'
                          f'{LOCATION_BUTTON}\n'
                          f'и отправить своё текущее местоположение\n'
                          f'или внизу экрана нажать на кнопку\n'
                          f'{ON_MAP_BUTTON}\n'
                          f'и выбрать место, где Вы хотите\n'
                          f'встретиться с курьером\n'
                          )

OTHER_CITY_MESSAGE = (f'{chr(0x2049)}Нам надо уточнить условия\n'
                      f'обмена в указанном городе\n'
                      f'Нажмите {SEND_ORDER_BUTTON}, \n'
                      f'чтобы мы могли с Вами связаться'
                      )

TIME_INTRO_MESSAGE = (f'{chr(0x231A)}Рабочее время курьеров:\n'
                      f'с 9:00 до 21:00.\n'
                      )

TIME_ERROR_MESSAGE = (f'{chr(0x2639)}\n'
                      f'К сожалению, сегодня курьер \n'
                      f'к Вам не успеет приехать\n'
                      f'Дата Вашей заявки изменена на завтра\n'
                      f'Учтите, что завтра курс может измениться'
                      )

TIME_START_MESSAGE = (f'{chr(0x1F570)} Вы будете ждать курьера с...'
                      )

TIME_END_MESSAGE = (f'{chr(0x1F570)} Вы будете ждать курьера до...'
                    )

CURRENCY_MESSAGE = (f'{chr(0x2754)} Вам удобнее указать сколько\n'
                    f'турецких лир Вы хотите купить\n'
                    f'или сколько российских рублей\n'
                    f'Вы хотите обменять на лиры?'
                    )

SHARE_CONTACT_MESSAGE = (f'Нажмите {SEND_ORDER_BUTTON}, \n'
                         f'чтобы мы могли с Вами связаться'
                         )
ORDER_COMPLETE_MESSAGE = (f'{chr(0x1F44D)} Ваша заявка принята, в ближайшее\n'
                          f'время с Вами свяжется менеджер'
                          )

LETS_START_AGAIN = (chr(0x1F44D) + " ОК, давайте начнем заново")

OK = chr(0x1F197)

MONEY_IN_HAND_IMG = Path(__file__).resolve().parent.parent / 'images' / 'money_in_hands.jpg'
GEO_INSTRUCTION_IMG = Path(__file__).resolve().parent.parent / 'images' / 'geo_instruction.jpg'

ADMIN_USER_ID = int(ADMIN_ID)


class FSMClient(StatesGroup):

    get_date = State()
    get_city = State()
    get_address = State()
    get_first_hour = State()
    get_second_hour = State()
    get_currency = State()
    get_money = State()
    get_money_limit = State()
    get_money_ok = State()
    send_order = State()


async def delete_stupid_message(msg):
    await bot.delete_message(msg.chat.id, msg.message_id)


async def delete_inline_keyboard(c_back):
    try:
        await c_back.message.edit_reply_markup(reply_markup=None)
    except:
        pass


async def delete_reply_button(msg):

    try:
        sent = await bot.send_message(msg.from_user.id,
                                      OK,
                                      reply_markup=ReplyKeyboardRemove()
                                      )
        await delete_stupid_message(sent)
    except:
        pass


async def start(msg):
    try:
        with open(MONEY_IN_HAND_IMG, 'rb') as image:
            await bot.send_photo(msg.from_user.id,
                                 image)

        await send_welcome(msg)

    except:
        await msg.reply(f'Общение с ботом только через личные сообщения.\n'
                        f'Напишите ему: https://t.me/alanya_lira_bot')


async def send_welcome(msg):

    answer = (f'Здравствуйте, {msg.from_user.first_name}.\n'
              f'Вас интересует курс на сегодня или на другой день?'
              )

    await bot.send_message(msg.from_user.id,
                           answer,
                           reply_markup=day_select_keyboard
                           )


async def handle_today(c_back: types.CallbackQuery, state: FSMContext):
    now_hour = datetime.now(timezone.utc).hour + 3
    if now_hour >= 20:

        await bot.send_message(c_back.from_user.id,
                               TIME_INTRO_MESSAGE
                               )
        await bot.send_message(c_back.from_user.id,
                               TIME_ERROR_MESSAGE
                               )
        tomorrow = datetime.now() + timedelta(days=1)
        order_day = tomorrow.strftime("%d.%m.%Y")
        async with state.proxy() as order:
            order["Дата"] = order_day

    else:
        today = datetime.now()
        order_day = today.strftime("%d.%m.%Y")
        async with state.proxy() as order:
            order["Дата"] = order_day

    await FSMClient.get_date.set()

    await delete_inline_keyboard(c_back)

    await bot.send_message(c_back.from_user.id,
                           CHOOSE_CITY_MESSAGE,
                           reply_markup=city_select_keyboard
                           )

    await FSMClient.next()


async def handle_other_day(c_back: types.CallbackQuery, state: FSMContext):
    name = c_back.from_user.first_name

    kurs_alanya = rate_db.read_rate('ALANYA')
    kurs_antalya = rate_db.read_rate('ANTALYA')


    answer = (f'На сегодня курс от {kurs_alanya} до {kurs_antalya},\n'
              f'в зависимости от города\n'
              f'{chr(0x303D)}  Но курс лиры меняется ежедневно.\n'
              f'{name}, сейчас Вы можете оставить заявку\n'
              f'и в указанный Вами день менеджер\n'
              f'свяжется с Вами и уточнит курс'
              )

    await delete_inline_keyboard(c_back)

    await bot.send_message(c_back.from_user.id,
                           answer,
                           reply_markup=await SimpleCalendar().start_calendar()
                           )


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data, state: FSMContext):

    today = date.today()
    today_formated = today.strftime("%d.%m.%Y")

    selected, data = await SimpleCalendar().process_selection(callback_query, callback_data)

    if selected:

        if data.date() <= today:
            answer = (
                f'{chr(0x2639)}\n'
                f'{callback_query.from_user.first_name}, Вам надо выбрать дату после {today_formated}'
            )
            await callback_query.message.edit_text(answer)

            await bot.send_message(callback_query.from_user.id,
                                   CHOOSE_DATE_MESSAGE,
                                   reply_markup=await SimpleCalendar().start_calendar()
                                   )
        else:
            await FSMClient.get_date.set()
            order_day = data.strftime('%d.%m.%Y')
            async with state.proxy() as order:
                order["Дата"] = order_day
                order["Day"] = int(data.strftime('%d'))

            await callback_query.message.edit_text(
                f'{chr(0x2713)} Вы выбрали {order["Дата"]}'
            )

            await bot.send_message(callback_query.from_user.id,
                                   CHOOSE_CITY_MESSAGE,
                                   reply_markup=city_select_keyboard
                                   )
            await FSMClient.next()


async def handle_city(c_back: types.CallbackQuery, state: FSMContext):
    city = c_back.data

    kurs_alanya = rate_db.read_rate('ALANYA')
    kurs_antalya = rate_db.read_rate('ANTALYA')

    if city == ANTALYA_BUTTON:
        kurs = kurs_antalya
        min_sum = 5000

    elif city == ALANYA_BUTTON:
        kurs = kurs_alanya
        min_sum = 'любая'

    else:
        kurs = kurs_antalya
        min_sum = 10000

    async with state.proxy() as order:
        order["Город"] = city
        order["Мин. сумма"] = min_sum
        order["Курс"] = kurs

    if order["Мин. сумма"] != "любая":
        min_sum = f'{order["Мин. сумма"]:_.0f}'.replace("_", " ")

    answer = (f'Сегодня курс в городе {city}:\n'
              f'{kurs} рублей за лиру.\n'
              f'Минимальная сумма сделки в лирах:\n'
              f'{min_sum}\n'
              f'Обмен происходит так:\n'
              f'при личной встрече с курьером\n'
              f'Вы переводите рубли с Вашей карты\n'
              f'на карту российского банка курьеру,\n'
              f'и он выдает Вам наличные лиры'
              )

    async with state.proxy() as order:

        today_flag = order["Дата"] == datetime.now().strftime("%d.%m.%Y")

        tomorrow = datetime.now() + timedelta(days=1)

        tomorrow_flag = order["Дата"] == tomorrow.strftime("%d.%m.%Y")

    if today_flag or tomorrow_flag:

        await delete_inline_keyboard(c_back)

        await bot.send_message(c_back.from_user.id,
                               answer
                               )

        await bot.send_message(c_back.from_user.id,
                               CHOOSE_ADDRESS_MESSAGE,
                               reply_markup=location_share_keyboard
                               )

        await FSMClient.next()

    else:

        await c_back.message.edit_text(f'{chr(0x2713)} Вы выбрали город {c_back.data}')

        await delete_inline_keyboard(c_back)

        await bot.send_message(c_back.from_user.id,
                               CURRENCY_MESSAGE,
                               reply_markup=currency_select_keyboard
                               )

        await FSMClient.get_currency.set()


async def handle_other_city(c_back: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as order:
        order["Город"] = c_back.data

    await delete_inline_keyboard(c_back)

    await bot.send_message(c_back.from_user.id,
                           OTHER_CITY_MESSAGE,
                           reply_markup=send_order_keyboard
                           )

    await FSMClient.send_order.set()


async def handle_location(msg: types.Message, state: FSMContext):
    async with state.proxy() as order:
        coordinates = f'{msg.location.latitude},{msg.location.longitude}'
        url = f'https://www.google.com/maps/place/{coordinates}'
        order["Геометка"] = url

    # await delete_reply_button(msg)

    answer = f'{chr(0x2713)} Вы указали местоположение на карте'

    await bot.send_message(msg.from_user.id,
                           text=answer,
                           reply_markup=ReplyKeyboardRemove()
                           )

    await bot.send_message(msg.from_user.id,
                           TIME_INTRO_MESSAGE
                           )

    await bot.send_message(msg.from_user.id,
                           TIME_START_MESSAGE,
                           reply_markup=first_hour_keyboard
                           )
    await FSMClient.get_first_hour.set()


async def handle_map(msg: types.Message, state: FSMContext):

    with open(GEO_INSTRUCTION_IMG, 'rb') as image:
        await bot.send_photo(msg.from_user.id,
                             image,
                             reply_markup=ReplyKeyboardRemove())


async def handle_venue(msg: types.Message, state: FSMContext):

    # venue: types.Venue = msg.venue

    async with state.proxy() as order:
        coordinates = f'{msg.location.latitude},{msg.location.longitude}'
        url = f'https://www.google.com/maps/place/{coordinates}'
        order["Геометка"] = url

    answer = f'{chr(0x2713)} Вы указали местоположение на карте'

    await bot.send_message(chat_id=msg.chat.id,
                           text=answer,
                           reply_markup=ReplyKeyboardRemove()
                           )

    await bot.send_message(chat_id=msg.chat.id,
                           text=TIME_INTRO_MESSAGE
                           )

    await bot.send_message(chat_id=msg.chat.id,
                           text=TIME_START_MESSAGE,
                           reply_markup=first_hour_keyboard
                           )
    await FSMClient.get_first_hour.set()


async def handle_address(msg: types.Message, state: FSMContext):
    async with state.proxy() as order:
        order["Адрес"] = msg.text

    answer = f'{chr(0x2713)} Вы указали адрес:\n{msg.text}'

    await bot.send_message(chat_id=msg.chat.id,
                           text=answer,
                           reply_markup=ReplyKeyboardRemove()
                           )

    await bot.send_message(msg.from_user.id,
                           TIME_INTRO_MESSAGE
                           )

    await bot.send_message(msg.from_user.id,
                           TIME_START_MESSAGE,
                           reply_markup=first_hour_keyboard
                           )

    await FSMClient.get_first_hour.set()


async def process_first_hour(c_back: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as order:

        today_flag = order["Дата"] == datetime.now().strftime("%d.%m.%Y")

    first_hour = int(c_back.data[7:])

    now_hour = datetime.now(timezone.utc).hour + 3

    time_is_low = first_hour < now_hour

    if today_flag and time_is_low:

        answer = (
            f'{chr(0x2639)}\n'
            f'{c_back.from_user.first_name}, Вам надо выбрать время\n'
            f'не раньше {now_hour}:00'
        )

        await delete_inline_keyboard(c_back)

        await bot.send_message(c_back.from_user.id,
                               answer,
                               reply_markup=first_hour_keyboard
                               )

    else:

        await c_back.message.edit_text(
                                       f'{chr(0x2713)} Вы будете ждать курьера с {first_hour}:00',
                                       )

        async with state.proxy() as order:
            order["Клиент ждёт с "] = first_hour

        await delete_inline_keyboard(c_back)

        await bot.send_message(c_back.from_user.id,
                               TIME_END_MESSAGE,
                               reply_markup=second_hour_keyboard
                               )

        await FSMClient.next()


async def process_second_hour(c_back: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as order:
        first_hour = order["Клиент ждёт с "]

    second_hour = int(c_back.data[7:])

    if second_hour <= first_hour:

        await delete_inline_keyboard(c_back)

        answer = (
            f'{chr(0x2639)}\n'
            f'{c_back.from_user.first_name}, Вам надо выбрать время\n'
            f'после {first_hour}:00'
        )
        await bot.send_message(c_back.from_user.id,
                               answer,
                               reply_markup=second_hour_keyboard
                               )
    else:

        await c_back.message.edit_text(
            f'{chr(0x2713)} Вы будете ждать курьера до {second_hour}:00',
        )

        async with state.proxy() as order:
            order["Клиент ждёт до "] = second_hour

        await delete_inline_keyboard(c_back)

        await bot.send_message(c_back.from_user.id,
                               CURRENCY_MESSAGE,
                               reply_markup=currency_select_keyboard
                               )

        await FSMClient.next()


async def handle_currency(c_back: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as order:
        if c_back.data == LIRAS_BUTTON:
            order["Указанная валюта"] = "турецкие лиры"
            if order["Мин. сумма"] == "любая":
                min_text = ''
            else:
                min_sum = f'{order["Мин. сумма"]:_.0f} лир'.replace("_", " ")
                min_text = f', не менее {min_sum}\n'
        elif c_back.data == ROUBLES_BUTTON:
            order["Указанная валюта"] = "российские рубли"
            if order["Мин. сумма"] == "любая":
                min_text = ''
            else:
                min_sum = f'{(order["Мин. сумма"] * order["Курс"]):_.2f} рублей'.replace("_", " ")
                min_text = f', не менее {min_sum}\n'
        order["Ограничение"] = min_text

    await delete_inline_keyboard(c_back)

    await c_back.message.edit_text(
        f'{chr(0x2713)} Вы выбрали {c_back.data}',
    )

    await bot.send_message(c_back.from_user.id,
                           f'{chr(0x1F4B0)} Теперь укажите сумму{min_text}',
                           reply_markup=ReplyKeyboardRemove()
                           )

    await FSMClient.next()


async def handle_money(msg: types.Message, state: FSMContext):
    async with state.proxy() as order:
        try:
            money = int(msg.text)
            if money <= 0:
                raise ValueError
            await FSMClient.next()
            await handle_money_limit(msg, money, state)

        except ValueError:
            answer = (f'{chr(0x2639)}\n'
                      f'Боту не удалось распознать сумму:\n'
                      f'{msg.text}\n'
                      f'Пожалуйста, используйте только цифры\n'
                      f'Теперь укажите сумму{order["Ограничение"]}'
                      )

            await bot.send_message(msg.from_user.id,
                                   answer
                                   )


async def handle_money_limit(msg: types.Message, money: int, state: FSMContext):
    async with state.proxy() as order:
        if order["Мин. сумма"] != "любая" and order["Указанная валюта"] == "турецкие лиры":
            if money >= order["Мин. сумма"]:
                await FSMClient.next()
                await handle_money_ok(msg, money, state)
            else:
                answer = (f'{chr(0x2639)}\n'
                          f'Для этого города должна быть\n'
                          f'указана сумма{order["Ограничение"]}'
                          )
                await FSMClient.get_money.set()
                await bot.send_message(msg.from_user.id,
                                       answer)
                await bot.send_message(msg.from_user.id,
                                       f'{chr(0x1F4B0)} Теперь укажите сумму{order["Ограничение"]}'
                                       )

        elif order["Мин. сумма"] != "любая" and order["Указанная валюта"] == "российские рубли":
            if money >= (order["Мин. сумма"] * order["Курс"]):
                await FSMClient.next()
                await handle_money_ok(msg, money, state)
            else:
                answer = (f'{chr(0x2639)}\n'
                          f'Для этого города должна быть \n'
                          f'указана сумма{order["Ограничение"]}'
                          )
                await FSMClient.get_money.set()
                await bot.send_message(msg.from_user.id,
                                       answer
                                       )
                await bot.send_message(msg.from_user.id,
                                       f'{chr(0x1F4B0)} Теперь укажите сумму{order["Ограничение"]}'
                                       )

        else:
            await FSMClient.next()
            await handle_money_ok(msg, money, state)


async def handle_money_ok(msg: types.Message, money: int, state: FSMContext):
    async with state.proxy() as order:

        today_flag = order["Дата"] == datetime.now().strftime("%d.%m.%Y")

        if order["Указанная валюта"] == "турецкие лиры":
            order["Указанная сумма"] = f'{msg.text} лир'

            answer_1 = f'{chr(0x1F44D)} Вы хотите купить {order["Указанная сумма"]}\n'

        if today_flag:
            answer_2 = (f'по курсу {order["Курс"]}\n'
                        f'Приготовьте {(money * order["Курс"]):_.2f} рублей\n'.replace("_", " ")
                        )
            answer_3 = ''
        else:
            answer_2 = ''
            answer_3 = f'{order["Дата"]} менеджер уточнит для Вас курс\n'

        if order["Указанная валюта"] == "российские рубли":

            money_ammount_1 = f'{msg.text} рублей\n'

            if today_flag:
                money_amount_2 = f'Это {(money / order["Курс"]):_.2f} лир\n'.replace("_", " ")
            else:
                money_amount_2 = ''

            order["Указанная сумма"] = money_ammount_1 + money_amount_2

            answer_1 = f'{chr(0x1F44D)} Вы хотите обменять {msg.text} рублей\n'

            if today_flag:
                answer_2 = (f'на {(money / order["Курс"]):_.2f} лир\n'.replace("_", " ") +
                            f'по курсу {order["Курс"]}\n')
                answer_3 = ''
            else:
                answer_2 = ''
                answer_3 = f'{order["Дата"]} менеджер уточнит для Вас курс\n'

    await bot.send_message(msg.from_user.id,
                           answer_1 + answer_2 + answer_3,
                           reply_markup=ReplyKeyboardRemove()
                           )

    await bot.send_message(msg.from_user.id,
                           SHARE_CONTACT_MESSAGE,
                           reply_markup=send_order_keyboard
                           )

    await FSMClient.next()


async def connect_to_manager(c_back: types.CallbackQuery, state: FSMContext):

    await delete_inline_keyboard(c_back)

    await bot.send_message(c_back.from_user.id,
                           SHARE_CONTACT_MESSAGE,
                           reply_markup=send_order_keyboard
                           )

    await FSMClient.send_order.set()


async def send_order_to_admin(msg: types.Message, state: FSMContext):
    async with state.proxy() as order:
        if msg.contact.first_name:
            order["Имя"] = msg.contact.first_name
        if msg.contact.last_name:
            order["Фамилия"] = msg.contact.last_name
        if msg.contact.phone_number:
            order["Телефон из Telegram"] = msg.contact.phone_number
        if msg.from_user.username:
            order["User name"] = f"@{msg.from_user.username}"
        order_message = ''

        for item in order:
            order_message += f'{str(item)} --- {str(order[item])}\n'

        await state.finish()
        await bot.send_message(ADMIN_USER_ID,
                               order_message
                               )

        if not msg.from_user.username:
            await bot.send_contact(ADMIN_USER_ID,
                                   phone_number=order["Телефон из Telegram"],
                                   first_name=order["Имя"]
                                   )

        await delete_reply_button(msg)

        await bot.send_message(msg.from_user.id,
                               ORDER_COMPLETE_MESSAGE,
                               reply_markup=welcome_keyboard
                               )


async def restart(c_back: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        await state.finish()

    await delete_inline_keyboard(c_back)

    await bot.send_message(c_back.from_user.id,
                           LETS_START_AGAIN,
                           reply_markup=ReplyKeyboardRemove()
                           )
    await send_welcome(c_back)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start,
                                commands=["start"],
                                state=None
                                )

    dp.register_message_handler(restart,
                                commands=["start"],
                                state="*"
                                )

    dp.register_callback_query_handler(start,
                                       lambda c: c.data == WELCOME_BUTTON,
                                       state=None
                                       )

    dp.register_callback_query_handler(start,
                                       lambda c: c.data == WELCOME_BUTTON,
                                       state="*"
                                       )

    dp.register_callback_query_handler(handle_today,
                                       lambda c: c.data == TODAY_BUTTON,
                                       state=None
                                       )

    dp.register_callback_query_handler(handle_other_day,
                                       lambda c: c.data == OTHER_DAY_BUTTON,
                                       state=None
                                       )

    dp.register_callback_query_handler(connect_to_manager,
                                       lambda c: c.data == MANAGER_BUTTON,
                                       state="*"
                                       )
    dp.register_message_handler(connect_to_manager,
                                Text(equals=MANAGER_BUTTON),
                                state="*"
                                )

    dp.register_callback_query_handler(restart,
                                       lambda c: c.data == RESTART_BUTTON,
                                       state="*"
                                       )

    dp.register_message_handler(restart,
                                Text(equals=RESTART_BUTTON),
                                state="*"
                                )

    dp.register_callback_query_handler(handle_city, lambda c: c.data == ANTALYA_BUTTON, state=FSMClient.get_city)
    dp.register_callback_query_handler(handle_city, lambda c: c.data == ALANYA_BUTTON, state=FSMClient.get_city)
    dp.register_callback_query_handler(handle_city, lambda c: c.data == BELEK_BUTTON, state=FSMClient.get_city)
    dp.register_callback_query_handler(handle_city, lambda c: c.data == SIDE_BUTTON, state=FSMClient.get_city)
    dp.register_callback_query_handler(handle_city, lambda c: c.data == KEMER_BUTTON, state=FSMClient.get_city)

    dp.register_callback_query_handler(handle_other_city,
                                       lambda c: c.data == OTHER_CITY_BUTTON,
                                       state=FSMClient.get_city
                                       )
    #   LOCATIONS
    #######################################################################
    dp.register_message_handler(handle_location,
                                content_types=["location"],
                                state=FSMClient.get_address
                                )
    #######################################################################
    dp.register_message_handler(handle_venue,
                                content_types=["venue"],
                                state=FSMClient.get_address
                                )
    #######################################################################
    dp.register_message_handler(handle_map,
                                Text(equals=ON_MAP_BUTTON),
                                state=FSMClient.get_address
                                )
    #######################################################################
    dp.register_message_handler(handle_address,
                                content_types=["text"],
                                state=FSMClient.get_address
                                )
    #######################################################################

    # TIME #

    dp.register_callback_query_handler(process_first_hour,
                                       lambda c: c.data.startswith("1_hour_"),
                                       state=FSMClient.get_first_hour
                                       )

    dp.register_callback_query_handler(process_second_hour,
                                       lambda c: c.data.startswith("2_hour_"),
                                       state=FSMClient.get_second_hour
                                       )

    # TIME #

    dp.register_callback_query_handler(handle_currency,
                                       lambda c: c.data == LIRAS_BUTTON,
                                       state=FSMClient.get_currency
                                       )

    dp.register_callback_query_handler(handle_currency,
                                       lambda c: c.data == ROUBLES_BUTTON,
                                       state=FSMClient.get_currency
                                       )

    #######################################################################
    dp.register_message_handler(handle_money,
                                content_types=["text"],
                                state=FSMClient.get_money
                                )
    ########################################################################

    dp.register_message_handler(handle_money_limit,
                                content_types=["text"],
                                state=FSMClient.get_money_limit
                                )
    #########################################################################
    dp.register_message_handler(handle_money_ok,
                                content_types=["text"],
                                state=FSMClient.get_money_ok
                                )
    #########################################################################

    dp.register_message_handler(send_order_to_admin,
                                content_types=["contact"],
                                state=FSMClient.send_order
                                )
    #########################################################################

    #   #   #   random_text_erasers #   #   #

    dp.register_message_handler(delete_stupid_message,
                                content_types=["text"],
                                state=None
                                )

    dp.register_message_handler(delete_stupid_message,
                                content_types=["text"],
                                state="*"
                                )
