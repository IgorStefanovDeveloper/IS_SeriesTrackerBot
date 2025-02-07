from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from bot.database import Database

class AddSeriesState(StatesGroup):
    waiting_for_series_name = State()
    waiting_for_seasons = State()

class NotifyState(StatesGroup):
    waiting_for_series_choice = State()
    waiting_for_notify_choice = State()

def setup_handlers(dp: Dispatcher, db: Database):
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        user_id = message.from_user.id
        username = message.from_user.username
        db.add_user(user_id, username)
        await message.answer("Добро пожаловать в Series Tracker Bot!")

    @dp.message_handler(commands=["add"])
    async def add_series_start(message: types.Message):
        await AddSeriesState.waiting_for_series_name.set()
        await message.answer("Введите название сериала:")

    @dp.message_handler(state=AddSeriesState.waiting_for_series_name)
    async def add_series_name(message: types.Message, state: FSMContext):
        series_name = message.text
        await state.update_data(series_name=series_name)
        await AddSeriesState.waiting_for_seasons.set()
        await message.answer("Сколько сезонов вы посмотрели?")

    @dp.message_handler(state=AddSeriesState.waiting_for_seasons)
    async def add_series_seasons(message: types.Message, state: FSMContext):
        try:
            seasons_watched = int(message.text)
            data = await state.get_data()
            series_name = data.get("series_name")
            user_id = message.from_user.id

            # Предполагается, что API-сервис возвращает API_ID сериала
            api_id = await fetch_series_api_id(series_name)
            db.add_series(user_id, series_name, api_id, seasons_watched)

            await state.finish()
            await message.answer(f"Сериал '{series_name}' добавлен!")
        except ValueError:
            await message.answer("Пожалуйста, введите число.")

    @dp.message_handler(commands=["list"])
    async def list_series(message: types.Message):
        user_id = message.from_user.id
        series_list = db.get_user_series(user_id)

        if not series_list:
            await message.answer("У вас нет добавленных сериалов.")
            return

        response = "Ваши сериалы:\n"
        for idx, (name, seasons_watched, episodes_watched, notify) in enumerate(series_list, 1):
            notify_status = "🔔" if notify else "🔕"
            response += f"{idx}. {name} - Сезонов: {seasons_watched}, Уведомления: {notify_status}\n"

        await message.answer(response)

    @dp.message_handler(commands=["notify"])
    async def notify_start(message: types.Message):
        user_id = message.from_user.id
        series_list = db.get_user_series(user_id)

        if not series_list:
            await message.answer("У вас нет добавленных сериалов.")
            return

        response = "Выберите сериал для изменения настроек уведомлений:\n"
        for idx, (name, _, _, _) in enumerate(series_list, 1):
            response += f"{idx}. {name}\n"

        await NotifyState.waiting_for_series_choice.set()
        await message.answer(response)

    @dp.message_handler(state=NotifyState.waiting_for_series_choice)
    async def notify_choose_series(message: types.Message, state: FSMContext):
        try:
            choice = int(message.text)
            series_list = db.get_user_series(message.from_user.id)
            if 1 <= choice <= len(series_list):
                series_name = series_list[choice - 1][0]
                series_id = db.get_series_id_by_name(series_name)
                await state.update_data(series_id=series_id)
                await NotifyState.waiting_for_notify_choice.set()
                await message.answer(f"Хотите получать уведомления о '{series_name}'? (да/нет)")
            else:
                await message.answer("Неверный выбор. Попробуйте снова.")
        except ValueError:
            await message.answer("Пожалуйста, введите число.")

    @dp.message_handler(state=NotifyState.waiting_for_notify_choice)
    async def notify_set_choice(message: types.Message, state: FSMContext):
        notify = message.text.lower() == "да"
        data = await state.get_data()
        series_id = data.get("series_id")
        user_id = message.from_user.id
        db.update_notify_flag(user_id, series_id, notify)
        await state.finish()
        await message.answer("Настройки уведомлений обновлены!")
