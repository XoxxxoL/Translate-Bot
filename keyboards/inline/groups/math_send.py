from aiogram import types
from loader import bot
import sqlite3 as sql
import random
import string
from handlers.groups import math_call
from utils import encode_int

global chat_link_ru
chat_link_ru = '@idle_city_free_chat_rus'


async def send_top():
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute("SELECT count, username FROM top ORDER BY count DESC")
    users = q.fetchall()
    text = (f'❤️ <a href="tg://user?id=341163252">XoxxxoL</a> навсегда в вашем сердешке\n'
            f"👑 Топ 10 игроков этого чата:\n"
            f'🥇 {users[0][1]} | ответов - {users[0][0]}\n'
            f'🥈 {users[1][1]} | ответов - {users[1][0]}\n'
            f'🥉 {users[2][1]} | ответов - {users[2][0]}\n'
            f'🍼 {users[3][1]} | ответов - {users[3][0]}\n'
            f'🍼 {users[4][1]} | ответов - {users[4][0]}\n'
            f'🍼 {users[5][1]} | ответов - {users[5][0]}\n'
            f'🍼 {users[6][1]} | ответов - {users[6][0]}\n'
            f'🍼 {users[7][1]} | ответов - {users[7][0]}\n'
            f'🍼 {users[8][1]} | ответов - {users[8][0]}\n'
            f'🍼 {users[9][1]} | ответов - {users[9][0]}\n')
    connection.close()
    await bot.send_message(chat_id=chat_link_ru, text=text)


async def send_math_message():
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute("SELECT id, m_id FROM game_history_ru WHERE close=0")
    open_game = q.fetchone()
    if open_game is not None:
        await bot.delete_message(chat_id=chat_link_ru, message_id=open_game[1])
        q.execute("UPDATE game_history_ru SET close=1 WHERE id='%s'" % (open_game[0]))
        connection.commit()
    type_game = random.randint(0, 1)
    if type_game == 1:
        act = random.choice(['+', '-', 'x'])
        if act == '-':
            f_num = random.randint(100, 20000)
            s_num = random.randint(10, f_num)
            answer = f_num - s_num
            act = '➖'
        elif act == '+':
            f_num = random.randint(10, 20000)
            s_num = random.randint(10, 20000)
            answer = f_num + s_num
        elif act == 'x':
            f_num = random.randint(2, 50)
            s_num = random.randint(2, 50)
            answer = f_num * s_num
        text = (f'🔢Весёлая математика🔢\n'
                f'Первый игрок👨‍🎓, правильно ответивший на вопрос, получает 🤑50к🤑\n\n'
                f'Пример: {f_num} {act} {s_num}\n\n'
                f'Ответ присылать в виде ![решение]')
        lol = await bot.send_message(chat_id=chat_link_ru, text=text)
        q.execute("INSERT INTO game_history_ru (answer, m_id, close) VALUES('%s', '%s', 0)" % (str(answer), lol.message_id))
        connection.commit()
        connection.close()
    elif type_game == 0:
        with open('russian_nouns.txt', encoding='utf-8') as file:
            text = file.read()
        text = text.split()
        word = random.choice(text)
        variant = ''.join(random.sample(word,  len(word)))
        if variant == word:
            variant = ''.join(random.sample(word,  len(word)))
        text = (f'🎮 Мини игра "Слова"\n'
                f'🔤 Ваша задач собрать слово из этих букв: <b>{variant}</b>'
                f'\n\nОтвет присылать в виде ![слово]')
        lol = await bot.send_message(chat_id=chat_link_ru, text=text)
        q.execute(f"INSERT INTO game_history_ru(answer, m_id) VALUES ('{word}', '{lol.message_id}')")
        connection.commit()
        connection.close()



# async def send_math_message_en():
#     connection = sql.connect('db.sql', check_same_thread=False)
#     q = connection.cursor()
#     q.execute("SELECT id, m_id FROM math_en WHERE close=0")
#     open_game = q.fetchone()
#     act = random.choice(['+', '-', 'x'])
#     if act == '-':
#         f_num = random.randint(10, 20000)
#         s_num = random.randint(10, 20000)
#         answer = f_num - s_num
#         act = '➖'
#     elif act == '+':
#         f_num = random.randint(10, 20000)
#         s_num = random.randint(10, 20000)
#         answer = f_num + s_num
#         act = '➕'
#     elif act == 'x':
#         f_num = random.randint(2, 50)
#         s_num = random.randint(2, 50)
#         answer = f_num * s_num
#         act = '✖️'
#     f_num_num = encode_int.encode(f_num)
#     s_num_num = encode_int.encode(s_num)
#     text = (f'🔢FUN MATH🔢\n'
#             f'The first player👨‍🎓 to answer the question correctly gets 🤑50k$🤑\n\n'
#             f'Example: {f_num_num} {act} {s_num_num}'
#             f'The response should be sent in the form of ![decision]')
#     if open_game is not None:
#         await bot.delete_message(chat_id='@idle_city_free_chat_en', message_id=open_game[1])
#         q.execute("UPDATE math_en SET close=1 WHERE id='%s'" % (open_game[0]))
#         connection.commit()
#         math_call.black_list_en.clear()
#     answer_call = ''.join(random.choice(string.ascii_letters) for _ in range(7))
#     lol = await bot.send_message(chat_id='@idle_city_free_chat_en', text=text)
#     q.execute("INSERT INTO math_en (f_num, s_num, answer, m_id, close) VALUES('%s', '%s', '%s', '%s', 0)" % (f_num, s_num, answer_call, lol.message_id))
#     connection.commit()
#     connection.close()
