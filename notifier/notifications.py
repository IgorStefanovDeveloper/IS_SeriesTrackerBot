import os
from aiogram import Bot
from notifier.scheduler import scheduler
from bot.database import Database

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)
db = Database()

async def check_new_episodes():
    print("Checking for new episodes...")
    all_users = db.get_all_users()
    for user in all_users:
        user_id = user["id"]
        series_list = db.get_user_series(user_id)

        for series in series_list:
            series_name, seasons_watched, _, notify = series
            if not notify:
                continue

            # Проверяем новые сезоны через API
            latest_season = await fetch_latest_season(series_name)
            if latest_season > seasons_watched:
                await bot.send_message(chat_id=user_id, text=f"Новый сезон доступен для {series_name}!")
