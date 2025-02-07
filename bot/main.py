import os
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from database import Database

# Получение переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Устанавливаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация базы данных
db = Database()

# Функция для получения информации о сериале
def get_series_info(series_name):
    try:
        # Запрос к api_service для получения данных о сериале
        response = requests.get(f'http://api_service:5000/get_series?name={series_name}')
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"API error: {response.status_code}")
            return {}
    except Exception as e:
        logging.error(f"Error in API request: {str(e)}")
        return {}

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    db.add_user(user_id, username)
    await message.reply("Привет! Я бот для отслеживания сериалов.")

# Команда /check_series
@dp.message_handler(commands=['check_series'])
async def check_series(message: types.Message):
    series_name = message.text.replace("/check_series", "").strip()
    if series_name:
        series_info = get_series_info(series_name)
        if series_info.get('results'):
            db.add_user_series(message.from_user.id, series_name)
            await message.reply(f"Подписан на сериал: {series_name}")
        else:
            await message.reply("Сериал не найден.")
    else:
        await message.reply("Введите название сериала после команды.")

# Команда /update_series
@dp.message_handler(commands=['update_series'])
async def update_series(message: types.Message):
    series_name = message.text.replace("/update_series", "").strip()
    if series_name:
        series_info = get_series_info(series_name)
        if series_info.get('results'):
            seasons_watched = 1  # Пример, можно добавить логику для получения сезона
            episodes_watched = 1  # Пример, можно добавить логику для получения эпизода
            db.update_user_series(message.from_user.id, series_name, seasons_watched, episodes_watched)
            await message.reply(f"Информация о сериале {series_name} обновлена!")
        else:
            await message.reply("Сериал не найден.")
    else:
        await message.reply("Введите название сериала после команды.")

# Команда /set_notify
@dp.message_handler(commands=['set_notify'])
async def set_notify(message: types.Message):
    try:
        series_name, notify = message.text.replace("/set_notify", "").strip().split()
        if series_name and notify in ['True', 'False']:
            db.update_notify(message.from_user.id, series_name, notify == 'True')
            await message.reply(f"Настройки уведомлений для сериала {series_name} обновлены на {notify}.")
        else:
            await message.reply("Неправильный формат команды.")
    except ValueError:
        await message.reply("Неправильный формат команды. Пример: /set_notify сериал True/False")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
