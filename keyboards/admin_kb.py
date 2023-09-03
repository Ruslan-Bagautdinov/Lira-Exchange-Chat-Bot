from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

KURS_ALANYA_ADMIN = 'Алания'
KURS_ANTALYA_ADMIN = 'Анталья'
CANCEL_ADMIN = 'Отмена'

adm_button_kurs_alanya = KeyboardButton(text=KURS_ALANYA_ADMIN)
adm_button_kurs_antalya = KeyboardButton(text=KURS_ANTALYA_ADMIN)
adm_button_cancel = KeyboardButton(text=CANCEL_ADMIN)


admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)

admin_keyboard.add(adm_button_kurs_alanya).insert(adm_button_kurs_antalya)
admin_keyboard.add(adm_button_cancel)
