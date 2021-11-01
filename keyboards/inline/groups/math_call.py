import time
import re

from aiogram import types
import sqlite3 as sql
from loader import bot

from loader import dp

global chat_link_ru

chat_link_ru = '@idle_city_free_chat_rus'


def calculate_time(time_mute):
    period = time_mute.split()[0]
    time = time_mute.split()[1]
    if period == 'm':
        time_mute = int(int(time) * 60)
    elif period == 'h':
        time_mute = int(int(time) * 3600)
    elif period == 'd':
        time_mute = int(int(time) * 86400)
    return time_mute



@dp.message_handler(commands=['ban'])
async def ban_user(message: types.Message):
    if message.from_user.id in [341163252, 678835170]:
        banned_user_id = message.reply_to_message
        banned_user_id = banned_user_id.from_user.id
        connection = sql.connect('db.sql', check_same_thread=False)
        q = connection.cursor()
        q.execute("INSERT INTO ban_user(user_id) VALUES ('%s')" % banned_user_id)
        connection.commit()
        connection.close()
        await message.answer('Пользователь забанен')

@dp.message_handler(commands=['unban'])
async def unban_user(message: types.Message):
    if message.from_user.id in [341163252, 678835170]:
        banned_user_id = message.reply_to_message
        banned_user_id = banned_user_id.from_user.id
        connection = sql.connect('db.sql', check_same_thread=False)
        q = connection.cursor()
        q.execute("DELETE FROM ban_user WHERE user_id='%s'" % banned_user_id)
        connection.commit()
        connection.close()
        await message.answer('Пользователь разбанен')


@dp.message_handler(commands='history')
async def game_history(message: types.Message):
    connection = sql.connect('db.sql', check_same_thread=False)
    q = connection.cursor()
    q.execute("SELECT answer, winner FROM game_history_ru WHERE close=1 ORDER BY id DESC LIMIT 5")
    data = q.fetchall()
    text = 'Последние 5 игр:\n'
    for d in data:
        if d[1] is None:
            text += f'❌ Ответ - {d[0]}\n'
        elif d[1] is not None:
            text += f'✅ Победитель - {d[1]}, ответ - {d[0]}\n'
    # text += '<code></code>'
    connection.close()
    await message.answer(text)


# @dp.message_handler(commands='top')
# async def top_for_math(message: types.Message):
#     chat_name = message.chat.title
#     # if chat_name == '🏙 Idle City free chat EN 🌆':
#     #     connection = sql.connect('db.sql', check_same_thread=False)
#     #     q = connection.cursor()
#     #     q.execute("SELECT count, username FROM top_math_en ORDER BY count DESC")
#     #     users = q.fetchall()
#     #     text = (f"👑 Top 3 mathematicians of this chat:\n"
#     #             f"👑 @XoxxxoL forever in your heart ❤️\n"
#     #             f'🥇 @{users[0][1]}\n'
#     #             f'🥈 @{users[1][1]}\n'
#     #             f'🥉 @{users[2][1]}\n')
#     #     await message.answer(text=text)
#     if chat_name == '🏙 Idle City free chat RU 🌆':
#


@dp.message_handler(commands='mute')
async def mute_user(message: types.Message):
    if message.from_user.id in [678835170, 87919728, 341163252]:
        time_mute = message.text.replace('/mute', '')
        time_calc = calculate_time(time_mute)
        period = time_mute.split()[0]
        time_mute = time_mute.split()[1]
        name = message.reply_to_message.from_user.full_name
        user_id = message.reply_to_message.from_user.id
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                        until_date = (int(time.time()) + int(time_calc)),
                                        can_send_messages=False,
                                        can_send_media_messages=False,
                                        can_send_other_messages=False,
                                        can_add_web_page_previews=False)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id, text= f'<a href="tg://user?id={user_id}">{name}</a> запрещено отправлять сообщения\n Надеюсь тебе хватит этого времени, чтобы подумать о своём поведении')


@dp.message_handler(commands='unmute')
async def unmute(message: types.Message):
    if message.from_user.id in [678835170, 87919728, 341163252]:
        name = message.reply_to_message.from_user.full_name
        user_id = message.reply_to_message.from_user.id
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                       can_send_messages=True,
                                       can_send_media_messages=True,
                                       can_send_other_messages=True,
                                       can_add_web_page_previews=True)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id, text=f'<a href="tg://user?id={user_id}">{name}</a> разблокирован.')


@dp.message_handler()
async def mess(message: types.Message):
    if message.chat.id == -1001498984500:
        if message.text.startswith('!'):
            answer = message.text.replace('!', '')
            answer = re.findall('\w', answer)
            answer = ''.join(answer)
            connection = sql.connect('db.sql', check_same_thread=False)
            q = connection.cursor()
            q.execute("SELECT user_id FROM ban_user WHERE user_id='%s'" % message.from_user.id)
            ban_user = q.fetchone()
            if ban_user is None:
                q.execute("SELECT answer, m_id FROM game_history_ru WHERE close=0")
                answer_db = q.fetchone()
                if answer_db is not None:
                    if answer.lower() == answer_db[0].lower():
                        username = message.from_user.first_name
                        q.execute("SELECT count FROM top WHERE  username='%s'" % username)
                        count = q.fetchone()
                        if count is None:
                            q.execute("INSERT INTO top(username, count) VALUES('%s', 1)" % username)
                            connection.commit()
                        elif count is not None:
                            q.execute("UPDATE top SET count='%s' WHERE username='%s'" % (count[0] + 1, username))
                            connection.commit()
                        await message.answer(f'✅ Правильный ответ: {answer}\n🎉 Победитель: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>\n\nСледующий розыгрыш через 15 минут! Выиграй 50К💰')
                        await bot.delete_message(chat_id=chat_link_ru, message_id=message.message_id)
                        await bot.delete_message(chat_id=chat_link_ru, message_id=answer_db[1])
                        q.execute(f"UPDATE game_history_ru SET winner='{message.from_user.first_name}', close=1 WHERE close=0")
                        connection.commit()
                        await bot.send_message(chat_id=-1001275597623, text=f'/math_reward_init {message.from_user.id}')
                    else:
                        await bot.delete_message(chat_id=chat_link_ru, message_id=message.message_id)
                connection.close()
            elif ban_user is not None:
                await bot.delete_message(chat_id=chat_link_ru, message_id=message.message_id)
