import sqlite3

conn = sqlite3.connect('jokes.db')
c = conn.cursor()
# Создаем таблицу, если она не существует

c.execute('''
CREATE TABLE IF NOT EXISTS jokes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    joke TEXT NOT NULL
)''')

conn.commit()
conn.close()