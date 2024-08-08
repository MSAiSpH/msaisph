import telebot
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен вашего бота
bot = telebot.TeleBot('7139744154:AAF1-RRSnZK-S7W66_8jy4sChqsvZy4vbT0')

# URL вашего локального WebApp (замените порт, если используете другой)
webapp_url = 'https://github.com/MSAiSpH/tg-scaner-bot.git'

# Словарь для хранения результатов сканирования
scan_results = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Сканировать QR-код", web_app=telebot.types.WebAppInfo(url=webapp_url)))
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

# Обработчик данных из WebApp
@bot.message_handler(content_types=['web_app_data'])
def handle_webapp_data(message):
    data = json.loads(message.web_app_data.data)

    if data['action'] == 'single_scan':
        # Обработка одиночного сканирования
        bot.send_message(message.chat.id, f"Результат сканирования: {data['result']}")
    elif data['action'] == 'multi_scan':
        # Обработка группового сканирования
        scan_results[message.chat.id] = data['results']
        bot.send_message(message.chat.id, "Результаты сохранены. Вы можете продолжить сканирование или завершить.")

        # Сохранение результатов в JSON файл (здесь реализуйте свою логику)
        with open("scan_results.json", "w") as f:
            json.dump(scan_results, f)

        # Отправка JSON файла пользователю
        bot.send_document(message.chat.id, open("scan_results.json", "rb"))

# Запуск бота
bot.polling()
