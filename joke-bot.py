import logging # отладка
#import requests # запросы по API
from telegram import Update # Обновления сообщений
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes # обработка команд
import random # рандом

TOKEN = '7915720272:AAG_hGluc5cY3wBcuievOhX0T70dY4yqqg0'

# Получаем анекдот из файла anek.txt
def get_joke():
    with open('anek.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    jokes = [j.strip() for j in content.split('\n\n') if j.strip()]
    return random.choice(jokes)

# Обработка /joke
async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke = get_joke()
    await update.message.reply_text(joke)

# Обработка /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я бот, который рассказывает анекдоты. Напиши /joke, чтобы услышать анекдот!')

# Запуск бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('joke', joke_command))
    app.add_handler(CommandHandler('start', start_command))
    
    print('Бот запущен!')
    app.run_polling()