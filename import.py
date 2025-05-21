import sqlite3

with open('anek.txt', 'r', encoding='utf-8') as file:
    jokes = [j.strip().replace('<|startoftext|>', '') for j in file.read().split('\n\n') if j.strip()]

conn = sqlite3.connect('jokes.db')
c = conn.cursor()

for joke in jokes:
    c.execute('INSERT INTO jokes (joke) VALUES (?)', (joke,))  # Имя поля text!

conn.commit()
conn.close()
