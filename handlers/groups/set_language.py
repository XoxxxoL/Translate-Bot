from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters

import filters

from loader import dp

import sqlite3 as sql


@dp.message_handler(lambda message: message.chat.type != 'private', lambda message: message.text.startswith('/set_lang1'), is_chat_admin=True)
async def voice(message: types.Message):
    """ Устанавливает первый язык для перевода в чате """
    text = message.text
    text = text.replace('/set_lang1', '')
    try:
        text = text.replace(' ', '')
    except:
        pass
    text = text.lower()
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute("SELECT chat_id FROM chats WHERE chat_id='%s'" % message.chat.id)
    lang = q.fetchone()
    if lang is None:
        q.execute("INSERT INTO chats(chat_id) VALUES('%s')" % message.chat.id)
        connection.commit()
    else:
        pass
    q.execute('UPDATE chats SET f_l="%s" WHERE chat_id="%s"' % (text, message.chat.id))
    connection.commit()
    connection.close()
    await message.reply('✅')


@dp.message_handler(lambda message: message.chat.type != 'private', lambda message: message.text.startswith('/set_lang2'), is_chat_admin=True)
async def voice(message: types.Message):
    """ Устанавливает второй язык для перевода в чате """
    text = message.text
    text = text.replace('/set_lang2', '')
    try:
        text = text.replace(' ', '')
    except:
        pass
    text = text.lower()
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute("SELECT chat_id FROM chats WHERE chat_id='%s'" % message.chat.id)
    lang = q.fetchone()
    if lang is None:
        q.execute("INSERT INTO chats(chat_id) VALUES('%s')" % message.chat.id)
        connection.commit()
    else:
        pass
    q.execute('UPDATE chats SET s_l="%s" WHERE chat_id="%s"' % (text, message.chat.id))
    connection.commit()
    connection.close()
    await message.reply('✅')



@dp.message_handler(lambda message: message.chat.type != 'private', lambda message: message.text.startswith('/set_video_lang'), is_chat_admin=True)
async def voice(message: types.Message):
    """ Устанавливает язык для перевода видео в чате """
    text = message.text
    text = text.replace('/set_video_lang', '')
    try:
        text = text.replace(' ', '')
    except:
        pass
    text = text.lower()
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute("SELECT chat_id FROM chats WHERE chat_id='%s'" % message.chat.id)
    lang = q.fetchone()
    if lang is None:
        q.execute("INSERT INTO chats(chat_id) VALUES('%s')" % message.chat.id)
        connection.commit()
    else:
        pass
    q.execute('UPDATE chats SET vn_l="%s" WHERE chat_id="%s"' % (text, message.chat.id))
    connection.commit()
    connection.close()
    await message.reply('✅')


@dp.message_handler(lambda message: message.chat.type != 'private', lambda message: message.text.startswith('/set_voice_lang'), is_chat_admin=True)
async def voice(message: types.Message):
    """ Устанавливает язык для первода голосовых сообщений """
    text = message.text
    text = text.replace('/set_voice_lang', '')
    try:
        text = text.replace(' ', '')
    except:
        pass
    text = text.lower()
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute("SELECT chat_id FROM chats WHERE chat_id='%s'" % message.chat.id)
    lang = q.fetchone()
    if lang is None:
        q.execute("INSERT INTO chats(chat_id) VALUES('%s')" % message.chat.id)
        connection.commit()
    else:
        pass
    q.execute('UPDATE chats SET v_l="%s" WHERE chat_id="%s"' % (text, message.chat.id))
    connection.commit()
    connection.close()
    await message.reply('✅')
