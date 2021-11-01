import sqlite3 as sql
import random


words = ['year', 'person', 'time', 'business', 'life', 'day', 'hand',
'once', 'Job', 'word', 'place', 'face', 'friend', 'eye', 'question',
'house', 'side', 'country', 'world', 'happening', 'head', 'child',
'force', 'end', 'view', 'system', 'part', 'town', 'attitude',
'female', 'money', 'Earth', 'car', 'water', 'father', 'problem',
'hour', 'право', 'leg', 'decision', 'Door', 'figure', 'story', 'power',
'law', 'war', 'God', 'vote', 'thousand', 'book', 'opportunity',
'result', 'night', 'table', 'name', 'region', 'article', 'number',
'company', 'people', 'wife', 'Group', 'development', 'process',
'court', 'condition', 'means', 'Start', 'shine', 'time', 'way',
'soul', 'level', 'form', 'connection', 'minute', 'street', 'evening',
'quality', 'think', 'road', 'mother', 'act', 'month', 'state',
'tongue', 'love', 'sight', 'mom', 'century', 'school', 'target', 'society',
'activity', 'organization', 'president', 'room', 'порядок', 'moment',
'theatre']

connection = sql.connect('db.sql', check_same_thread=False)
q = connection.cursor()
q.execute('SELECT COUNT(rus) FROM words')
count = q.fetchone()[0]
id_word = random.randint(1, count)
q.execute(f"SELECT rus FROM words WHERE id='{id_word}'")
word = q.fetchone()[0]
print(len(word))
a = 0
random_words = []
while a != 3:
    id_word_random = random.randint(1, count)
    q.execute(f"SELECT rus FROM words WHERE id='{id_word_random}'")
    random_words.append(q.fetchone()[0])
    a += 1
word_list = list(word)
variant = ''.join(random.sample(word_list,  len(word_list)))
q.execute(f"INSERT INTO words_history('{word}')")
connection.commit()
connection.close()
await await bot.send_message('text', reply_markup=keyb(answer, random_words))



# a = 1
# for w in words:
#     q.execute(f"UPDATE words SET en='{w}' WHERE id='{a}'")
#     connection.commit()
#     a += 1
# connection.close()
