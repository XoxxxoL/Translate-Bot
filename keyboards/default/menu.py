from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard_gen(lang):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        change = KeyboardButton('Сменить язык')
        help = KeyboardButton('Как это работает?')
    elif lang == 'en':
        help = KeyboardButton('How it works?')
        change = KeyboardButton('Change language')
    keyb.add(help)
    keyb.insert(change)
    return keyb
