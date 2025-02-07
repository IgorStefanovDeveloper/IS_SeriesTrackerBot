import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.database import Database
from bot.handlers import setup_handlers

# Инициализация бота
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Подключение к базе данных
db = Database()

# Настройка обработчиков команд
setup_handlers(dp, db)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
