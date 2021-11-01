from langdetect import detect
from deep_translator import GoogleTranslator
import sqlite3 as sql
from pydub import AudioSegment
import speech_recognition as sr

import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters

import filters

from loader import dp


@dp.message_handler(lambda message: message.chat.type != 'private', content_types=types.ContentTypes.VOICE)
async def voice(message: types.Message):
    """ Переводит голосовое сообщение """
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute(f"SELECT v_l, v_l1 FROM chats WHERE chat_id='{message.chat.id}'")
    result = q.fetchone()
    if result[0] is None:
        q.execute("INSERT INTO chats(chat_id) VALUES('%s')" % message.chat.id)
        connection.commit()
    elif result[0] != 'none':
        await dp.bot.send_chat_action(message.chat.id, 'typing')
        name = str(message.chat.id).replace('-', '')
        await message.voice.download(f'{name}.ogg')
        AudioSegment.from_ogg(f'{name}.ogg').export(f'{name}.wav', format='wav')
        r = sr.Recognizer()
        harvard = sr.AudioFile(f'{name}.wav')
        with harvard as source:
            music = r.record(source)
        await dp.bot.send_chat_action(message.chat.id, 'typing')
        audio = r.recognize_google(music, language='ru', show_all=True)
        # text = GoogleTranslator(source='auto', target=lang1).translate(audio)
        await message.answer(audio)
        os.remove(f"{name}.wav")
    else:
        pass
    connection.close()
