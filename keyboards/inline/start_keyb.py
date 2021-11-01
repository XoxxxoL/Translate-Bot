from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback import st_callback

start_k = InlineKeyboardMarkup()
russian = InlineKeyboardButton('🇷🇺 Русский', callback_data=st_callback.new(lang='ru'))
english = InlineKeyboardButton('🇬🇧 English', callback_data=st_callback.new(lang='en'))
start_k.add(russian, english)
