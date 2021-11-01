from langdetect import detect
from deep_translator import GoogleTranslator
import sqlite3 as sql
import subprocess
import os
import re
import speech_recognition as sr

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters

import filters

from loader import dp



@dp.message_handler(lambda message: message.chat.type != 'private', content_types=types.ContentTypes.VIDEO)
async def translate_video_auidio(message: types.Message):
    """ Переводит обычное видео """
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute(f"SELECT vn_l FROM chats WHERE chat_id='{message.chat.id}'")
    lang = q.fetchone()
    if lang is None:
        q.execute("INSERT INTO chats(chat_id) VALUES('%s')" % message.chat.id)
        connection.commit()
        lang = 'none'
    else:
        lang = lang[0]
    if lang != 'none':
        await dp.bot.send_chat_action(message.chat.id, 'typing')
        name = str(message.chat.id).replace('-', '')
        await message.video.download(f'{name}.mp4')
        command = f"ffmpeg -i {name}.mp4 -ab 160k -ac 2 -ar 44100 -vn {name}_video.wav"
        subprocess.call(command, shell=True)
        os.remove(f"{name}.mp4")
        r = sr.Recognizer()
        harvard = sr.AudioFile(f'{name}_video.wav')
        with harvard as source:
            audio = r.record(source)
        audio = r.recognize_google(audio, language='ru')
        # text = ts.google(audio, to_language=lang, if_use_cn_host=False)
        text = GoogleTranslator(source='auto', target=lang).translate(audio)
        os.remove(f"{name}_video.wav")
        await message.reply(f'Оригинал: {audio}\n\nTrasnlate: {text}')
    else:
        pass
    connection.close()



@dp.message_handler(lambda message: message.chat.type != 'private', content_types=types.ContentTypes.VIDEO_NOTE)
async def translate_video_auidio(message: types.Message):
    """ Переводит видео в кружочке """
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute(f"SELECT vn_l FROM chats WHERE chat_id='{message.chat.id}'")
    lang = q.fetchone()
    if lang is None:
        q.execute("INSERT INTO chats(chat_id) VALUES('%s')" % message.chat.id)
        connection.commit()
        lang = 'none'
    else:
        lang = lang[0]
    if lang != 'none':
        await dp.bot.send_chat_action(message.chat.id, 'typing')
        name = str(message.chat.id).replace('-', '')
        await message.video_note.download(f'{name}_note.mp4')
        command = f"ffmpeg -i {name}_note.mp4 -ab 160k -ac 2 -ar 44100 -vn {name}_video_note.wav"
        subprocess.call(command, shell=True)
        os.remove(f"{name}_note.mp4")
        r = sr.Recognizer()
        harvard = sr.AudioFile(f'{name}_video_note.wav')
        with harvard as source:
            audio = r.record(source)
        audio = r.recognize_google(audio, language='ru')
        text = GoogleTranslator(source='auto', target=lang).translate(audio)
        os.remove(f"{name}_video_note.wav")
        await message.reply(f'Оригинал: {audio}\n\nTrasnlate: {text}')
    else:
        pass
    connection.close()
