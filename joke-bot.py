import logging # отладка
#import requests # запросы по API
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup # Обновления сообщений
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler # обработка команд
import random # рандом
import os # TOKEN
import sqlite3 # база данных

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Получаем анекдот из файла anek.txt
def get_joke():

    #with open('anek.txt', 'r', encoding='utf-8') as file:
       # content = file.read()
    #jokes = [j.strip().replace('<|startoftext|>', '') for j in content.split('\n\n') if j.strip()]
    #return random.choice(jokes)

    conn = sqlite3.connect('jokes.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM jokes')
    count = c.fetchone()[0]
    if count == 0:
        conn.close()
        return "Нет анекдотов в базе данных."
    random_id = random.randint(1, count)
    c.execute(f'SELECT joke FROM jokes WHERE id={random_id}')
    row = c.fetchone()
    conn.close()
    if row:
       return row[0]
    else:
        return "Нет анекдотов в базе данных."





# Обработка /joke
async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("Анекдот!", callback_data='joke')   
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message: 
        await update.message.reply_text('Нажми кнопку, чтобы услышать анекдот!', reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text('Нажми кнопку, чтобы услышать анекдот!', reply_markup=reply_markup)
  # Обработка нажатия на кнопку "Анекдот!"

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'joke':
        joke = get_joke()
        keyboard = [[
            InlineKeyboardButton("Анекдот!", callback_data='joke')   
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(joke, reply_markup=reply_markup)



# Обработка /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я бот, который рассказывает анекдоты. Напиши /joke, чтобы услышать анекдот!')

# Запуск бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('joke', joke_command))
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print('Бот запущен!')
    app.run_polling()