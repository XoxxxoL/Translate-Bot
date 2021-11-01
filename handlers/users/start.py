from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import filters

from loader import dp

from keyboards.inline.callback import st_callback
from keyboards.inline.start_keyb import start_k
from keyboards.default.menu import keyboard_gen
import sqlite3 as sql



@dp.message_handler(CommandStart(), lambda message: message.chat.type == 'private')
async def start(message: types.Message):
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute("SELECT language FROM users WHERE t_id='%s'" % message.from_user.id)
    res = q.fetchone()
    if res is None:
        q.execute("INSERT INTO users(t_id) VALUES('%s')" % message.from_user.id)
        connection.commit()
        await message.answer(f'👋 Привет, {message.from_user.full_name}, выбери удобный для тебя язык на клавиатуре 👇\n\n'
                             f'👋 Hi, {message.from_user.full_name}, Choose a handbook convenient for you on the keyboard 👇', reply_markup=start_k)
    elif res is not None:
        if res[0] == 'ru':
            await message.answer(f'👋 Привет, {message.from_user.full_name}, выбери интересующее тебя действие на клавиатуре ниже 👇', reply_markup=keyboard_gen(res[0]))
        elif res[0] == 'en':
            await message.answer(f'👋 Hi, {message.from_user.full_name}, choose the action of the keypad on the keyboard below. 👇', reply_markup=keyboard_gen(res[0]))
    connection.close()


@dp.message_handler(filters.Text(equals='Как это работает?'), lambda message: message.chat.type == 'private')
async def kak_rab(message: types.message):
    text = ('👋 Привет, я переводчик для чатов.\n'
            '❗️ Что я умею:\n\n'
            '🔘 Переводить текстовые сообщения с одного языка на другой и в обратную сторону\n'
            '🔘 Переводить текст голосовых сообщений на выбранный язык\n'
            '🔘 Переводить текст обычных видео и видео в кружке на выбранный язык\n\n'
            'Для начала использования, добавь меня в чат и выдай доступ к сообщениям (выдай админку в чате), после чего, командами установи языки для перевода (команды вводить в чате):\n\n'
            '/set_language1 [язык] - первый язык для перевода текста\n'
            '/set_language2 [язык] - второй язык для перевода текста\n'
            '/set_voice_lang [язык] - язык для перевода голосовых\n'
            '/set_video_lang [язык] - язык для перевода видео\n\n'
            'Пример - /set_language1 ru\n'
            'Чтобы остановить перевод одного из типа сообщений, вместо языка, укажи none\n'
            'Пример - /set_voice_lang none')
    await message.answer(text, reply_markup=keyboard_gen('ru'))


@dp.message_handler(filters.Text(equals=['Сменить язык', 'Change language']), lambda message: message.chat.type == 'private')
async def change_language_rus(message: types.message):
    await message.answer(f'👋 Привет, {message.from_user.full_name}, выбери удобный для тебя язык на клавиатуре 👇\n\n'
                         f'👋 Hi, {message.from_user.full_name}, Choose a handbook convenient for you on the keyboard 👇', reply_markup=start_k)


@dp.message_handler(filters.Text(equals='How it works?'), lambda message: message.chat.type == 'private')
async def what(message: types.Message):
    text = ('👋 Hi, I am a chat translator.\n'
            '❗️ What I know:\n\n'
            '🔘 Translate text messages from one language to another and in the opposite direction\n'
            '🔘 Translate text voice messages to the selected language\n'
            '🔘 Translate text of regular video and video in a mug to the selected language\n\n'
            'To begin use, add me to the chat and issue access to messages (issue an admin in chat), after which commands set languages for translation (commands in chat):\n\n'
            '/set_language1 [language] - first language for text translation\n'
            '/set_language2 [language] - second language for text translation\n'
            '/set_voice_lang [language] - language for translation voice\n'
            '/set_video_lang [language] - language for translation video\n\n'
            'Example - /set_language1 ru\n'
            'To stop the translation of one of the type of messages, instead of language, indicate none\n'
            'Example - /set_voice_lang none')
    await message.answer(text, reply_markup=keyboard_gen('en'))


@dp.callback_query_handler(st_callback.filter())
async def set_main_lang(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    lang = callback_data.get('lang')
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute('UPDATE users SET language="%s" WHERE t_id="%s"' % (lang, call.from_user.id))
    connection.commit()
    connection.close()
    if lang == 'ru':
        await call.message.answer(f'👋 Привет, {call.from_user.full_name}, выбери интересующее тебя действие на клавиатуре ниже 👇', reply_markup=keyboard_gen(lang))
    elif lang == 'en':
        await call.message.answer(f'👋 Hi, {call.from_user.full_name}, choose the action of the keypad on the keyboard below. 👇', reply_markup=keyboard_gen(lang))
