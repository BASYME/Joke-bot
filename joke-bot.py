import sqlite3
import os
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# --- Клавиатура ---
keyboard = [
    [KeyboardButton("Анекдот!"), KeyboardButton("Свежий анекдот с сайта")],
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# --- Получить анекдот из файла ---
def get_joke():
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



# --- Получить анекдот с сайта ---
def get_fresh_joke():
    try:
        url = 'https://www.anekdot.ru/random/anekdot/'
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        jokes_divs = soup.find_all('div', class_='text')
        jokes = [div.get_text(strip=True) for div in jokes_divs]
        return random.choice(jokes) if jokes else "Не удалось получить свежий анекдот."
    except Exception:
        return "Ошибка при получении анекдота с сайта."

# --- /start ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-анекдотчик. Жми на кнопки внизу 👇",
        reply_markup=reply_markup
    )

# --- Обработка сообщений ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "Анекдот!":
        await update.message.reply_text(get_joke(), reply_markup=reply_markup)
    elif text == "Свежий анекдот с сайта":
        await update.message.reply_text(get_fresh_joke(), reply_markup=reply_markup)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print('Bot started!')
    app.run_polling()
