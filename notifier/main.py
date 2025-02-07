import os
import logging
import requests
from aiogram import Bot
from scheduler import scheduler
from bot.database import Database

# Получаем токен из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Инициализация базы данных
db = Database()

# Функция для получения информации о новых сезонах
async def fetch_latest_season(series_name):
    """
    Функция делает запрос к API (например, api_service) для получения информации о последнем сезоне сериала.
    """
    try:
        response = requests.get(f'http://api_service:5000/get_series?name={series_name}')
        data = response.json()
        # Пример предполагаемого формата ответа от API
        if 'results' in data:
            latest_season = data['results'][0].get('last_season', 0)
            return latest_season
        return 0
    except Exception as e:
        logging.error(f"Error fetching latest season for {series_name}: {e}")
        return 0

# Функция для проверки новых серий
async def check_new_episodes():
    """
    Проверяет наличие новых сезонов для сериалов у всех пользователей и отправляет уведомления, если новый сезон доступен.
    """
    logging.info("Checking for new episodes...")

    # Получаем всех пользователей из базы данных
    all_users = db.get_all_users()

    for user in all_users:
        user_id = user["id"]

        # Получаем сериалы пользователя
        series_list = db.get_user_series(user_id)

        for series in series_list:
            series_name, seasons_watched, _, notify = series

            # Если уведомления отключены для этого сериала, пропускаем
            if not notify:
                continue

            # Получаем информацию о последнем сезоне через API
            latest_season = await fetch_latest_season(series_name)

            # Если найден новый сезон, отправляем уведомление пользователю
            if latest_season > seasons_watched:
                message = f"Новый сезон доступен для {series_name}! Сезон {latest_season}"
                await bot.send_message(chat_id=user_id, text=message)

# Планируем выполнение функции check_new_episodes каждую минуту
scheduler.add_job(check_new_episodes, 'interval', minutes=10)

if __name__ == '__main__':
    # Запускаем планировщик задач
    logging.info("Starting scheduler...")
    scheduler.start()
