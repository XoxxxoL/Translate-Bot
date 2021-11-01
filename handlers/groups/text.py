from langdetect import detect
from deep_translator import GoogleTranslator
import sqlite3 as sql

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters

import filters

from loader import dp


@dp.message_handler(lambda message: message.chat.type != 'private', content_types=types.ContentTypes.PHOTO|types.ContentTypes.DOCUMENT)
async def translate_text_under_photo(message: types.Message):
    """ Переводит подпись под фото или документом """
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute(f"SELECT f_l, s_l FROM chats WHERE chat_id='{message.chat.id}'")
    lang = q.fetchone()
    if lang is None:
        q.execute("INSERT INTO chats(chat_id) VALUES('%s')" % message.chat.id)
        connection.commit()
        lang = 'none'
    else:
        pass
    if len(lang) > 1:
        if lang[0] == 'none' or lang[1] == 'none':
            return
        else:
            await dp.bot.send_chat_action(message.chat.id, 'typing')
            text_message = message.caption
            indetect = detect(text_message)
            if indetect == lang[0]:
                langout = lang[1]
            else:
                langout = lang[0]
            text = GoogleTranslator(source='auto', target=langout).translate(text_message)
            await message.reply(text)
    else:
        pass


@dp.message_handler(lambda message: message.chat.type != 'private', content_types=types.ContentTypes.TEXT)
async def test(message: types.Message):
    """ Переводит обычное текстовое сообщение """
    if message.text.startswith('/') or message.text.startswith('@'):
        return
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute(f"SELECT f_l, s_l FROM chats WHERE chat_id='{message.chat.id}'")
    lang = q.fetchone()
    if lang is None:
        q.execute("INSERT INTO chats(chat_id) VALUES('%s')" % message.chat.id)
        connection.commit()
        lang = 'none'
    else:
        pass
    if lang[0] == 'none' or lang[1] == 'none' or lang == 'none':
        return
    else:
        await dp.bot.send_chat_action(message.chat.id, 'typing')
        text_message = message.text
        ms = detect(text_message)
        if ms == lang[0]:
            longout = lang[1]
            text = GoogleTranslator(source='ru', target=longout).translate(text_message)
        elif ms == lang[1]:
            longout = lang[0]
            text = GoogleTranslator(source='auto', target=longout).translate(text_message)
        elif ms != lang[0] and ms != lang[1]:
            return
        await message.reply(f"{text}")
