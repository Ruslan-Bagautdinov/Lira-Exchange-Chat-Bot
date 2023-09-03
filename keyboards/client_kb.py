from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# BUTTONS_TEXT
WELCOME_BUTTON = chr(0x1F44B) + ' Начать диалог'
MANAGER_BUTTON = chr(0x2139) + ' Связаться с менеджером'
RESTART_BUTTON = chr(0x1F504) + ' Начать заново'

TODAY_BUTTON = chr(0x2600) + ' Сегодня'
OTHER_DAY_BUTTON = chr(0x1F4C5) + ' В другой день'

ANTALYA_BUTTON = chr(0x1F3D6) + ' Анталия'
ALANYA_BUTTON = chr(0x1F3D6) + ' Алания'
KEMER_BUTTON = chr(0x1F3D6) + ' Кемер'
SIDE_BUTTON = chr(0x1F3D6) + ' Сиде'
BELEK_BUTTON = chr(0x1F3D6) + ' Белек'
OTHER_CITY_BUTTON = chr(0x2753) + 'Другой город'

ON_MAP_BUTTON = chr(0x1F5FA) + ' УКАЗАТЬ НА КАРТЕ'
LOCATION_BUTTON = chr(127758) + ' ПОДЕЛИТЬСЯ МЕСТОПОЛОЖЕНИЕМ'


LIRAS_BUTTON = chr(0x1F1F9) + chr(0x1F1F7) + ' Турецкие лиры'
ROUBLES_BUTTON = chr(0x1F1F7) + chr(0x1F1FA) + ' Российские рубли'

SEND_ORDER_BUTTON = chr(128222) + ' ПОДЕЛИТЬСЯ TELEGRAM'


# universal_buttons
manager_button = InlineKeyboardButton(MANAGER_BUTTON, callback_data=MANAGER_BUTTON)

inline_restart_button = InlineKeyboardButton(RESTART_BUTTON, callback_data=RESTART_BUTTON)
reply_restart_button = KeyboardButton(RESTART_BUTTON)


# keyboards

#  ____________________________________WELCOME_________________________________________

welcome_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True,
                                        row_width=1
                                        )
welcome_button = InlineKeyboardButton(WELCOME_BUTTON, callback_data=WELCOME_BUTTON)

welcome_keyboard.add(welcome_button)


#  ____________________________________DAY SELECT_________________________________________


day_select_keyboard = InlineKeyboardMarkup(one_time_keyboard=True,
                                           row_width=4
                                           )

today_button = InlineKeyboardButton(TODAY_BUTTON, callback_data=TODAY_BUTTON)
other_day_button = InlineKeyboardButton(OTHER_DAY_BUTTON, callback_data=OTHER_DAY_BUTTON)

day_select_keyboard.add(today_button).insert(other_day_button)
day_select_keyboard.add(manager_button)

#  ____________________________________CITY SELECT_________________________________________

city_select_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                            one_time_keyboard=True,
                                            row_width=4
                                            )
antalya_city_button = InlineKeyboardButton(ANTALYA_BUTTON, callback_data=ANTALYA_BUTTON)
alanya_city_button = InlineKeyboardButton(ALANYA_BUTTON, callback_data=ALANYA_BUTTON)
kemer_city_button = InlineKeyboardButton(KEMER_BUTTON, callback_data=KEMER_BUTTON)
side_city_button = InlineKeyboardButton(SIDE_BUTTON, callback_data=SIDE_BUTTON)
belek_city_button = InlineKeyboardButton(BELEK_BUTTON, callback_data=BELEK_BUTTON)
other_city_button = InlineKeyboardButton(OTHER_CITY_BUTTON, callback_data=OTHER_CITY_BUTTON)

city_select_keyboard.add(alanya_city_button).insert(antalya_city_button).insert(kemer_city_button)
city_select_keyboard.add(belek_city_button).insert(side_city_button).insert(other_city_button)


#  ____________________________________LOCATION SHARE_________________________________________

location_share_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                              one_time_keyboard=True
                                              )

location_button = KeyboardButton(LOCATION_BUTTON,
                                 request_location=True)

on_map_button = KeyboardButton(ON_MAP_BUTTON)

location_share_keyboard.add(location_button)\
    .add(on_map_button)


#  ____________________________________FIRST HOUR_________________________________________

first_hour_keyboard = InlineKeyboardMarkup(row_width=4)
first_button_9 = InlineKeyboardButton("9:00", callback_data="1_hour_9")
first_button_10 = InlineKeyboardButton("10:00", callback_data="1_hour_10")
first_button_11 = InlineKeyboardButton("11:00", callback_data="1_hour_11")
first_button_12 = InlineKeyboardButton("12:00", callback_data="1_hour_12")
first_button_13 = InlineKeyboardButton("13:00", callback_data="1_hour_13")
first_button_14 = InlineKeyboardButton("14:00", callback_data="1_hour_14")
first_button_15 = InlineKeyboardButton("15:00", callback_data="1_hour_15")
first_button_16 = InlineKeyboardButton("16:00", callback_data="1_hour_16")
first_button_17 = InlineKeyboardButton("17:00", callback_data="1_hour_17")
first_button_18 = InlineKeyboardButton("18:00", callback_data="1_hour_18")
first_button_19 = InlineKeyboardButton("19:00", callback_data="1_hour_19")
first_button_20 = InlineKeyboardButton("20:00", callback_data="1_hour_20")
# first_button_21 = InlineKeyboardButton("21:00", callback_data="1_hour_21")

first_hour_keyboard.add(first_button_9).insert(first_button_10).insert(first_button_11).insert(first_button_12)
first_hour_keyboard.add(first_button_13).insert(first_button_14).insert(first_button_15).insert(first_button_16)
first_hour_keyboard.add(first_button_17).insert(first_button_18).insert(first_button_19).insert(first_button_20)
first_hour_keyboard.add(inline_restart_button)

#  ____________________________________SECOND HOUR_________________________________________

second_hour_keyboard = InlineKeyboardMarkup(row_width=4)
second_button_9 = InlineKeyboardButton("9:00", callback_data="2_hour_9")
second_button_10 = InlineKeyboardButton("10:00", callback_data="2_hour_10")
second_button_11 = InlineKeyboardButton("11:00", callback_data="2_hour_11")
second_button_12 = InlineKeyboardButton("12:00", callback_data="2_hour_12")
second_button_13 = InlineKeyboardButton("13:00", callback_data="2_hour_13")
second_button_14 = InlineKeyboardButton("14:00", callback_data="2_hour_14")
second_button_15 = InlineKeyboardButton("15:00", callback_data="2_hour_15")
second_button_16 = InlineKeyboardButton("16:00", callback_data="2_hour_16")
second_button_17 = InlineKeyboardButton("17:00", callback_data="2_hour_17")
second_button_18 = InlineKeyboardButton("18:00", callback_data="2_hour_18")
second_button_19 = InlineKeyboardButton("19:00", callback_data="2_hour_19")
second_button_20 = InlineKeyboardButton("20:00", callback_data="2_hour_20")
second_button_21 = InlineKeyboardButton("21:00", callback_data="2_hour_21")

second_hour_keyboard.add(second_button_9).insert(second_button_10).insert(second_button_11).insert(second_button_12)
second_hour_keyboard.add(second_button_13).insert(second_button_14).insert(second_button_15).insert(second_button_16)
second_hour_keyboard.add(second_button_17).insert(second_button_18).insert(second_button_19).insert(second_button_20)
second_hour_keyboard.add(second_button_21)\
    .add(inline_restart_button)

#  ____________________________________CURRENCY SELECT_________________________________________

currency_select_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                                one_time_keyboard=True
                                                )
liras_button = InlineKeyboardButton(LIRAS_BUTTON, callback_data=LIRAS_BUTTON)
roubles_button = InlineKeyboardButton(ROUBLES_BUTTON, callback_data=ROUBLES_BUTTON)
currency_select_keyboard.add(liras_button).insert(roubles_button)


#  ____________________________________SEND ORDER_________________________________________

send_order_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                          one_time_keyboard=True
                                          )

send_order_button = KeyboardButton(SEND_ORDER_BUTTON,
                                   callback_data=SEND_ORDER_BUTTON,
                                   request_contact=True,
                                   one_time_keyboard=True
                                   )
send_order_keyboard.add(send_order_button)
send_order_keyboard.add(reply_restart_button)


#  ____________________________________RESTART_________________________________________

restart_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True
                                        )
restart_keyboard.add(inline_restart_button)


#  ____________________________________MANAGER_________________________________________

manager_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True
                                        )
manager_keyboard.add(manager_button).add(inline_restart_button)
