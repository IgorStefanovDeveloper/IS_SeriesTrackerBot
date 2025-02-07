# Series Tracker Bot

## Описание
Telegram-бот для отслеживания сериалов. Пользователи могут добавлять сериалы в свой список, указывать количество просмотренных сезонов и получать уведомления о выходе новых эпизодов.

---

## Стек технологий
- **Python** (aiogram, psycopg2, aiohttp, apscheduler)
- **PostgreSQL** (для хранения данных пользователей и сериалов)
- **Redis** (для кэширования данных API)
- **Docker** (для контейнеризации)
- **TMDb API** (для получения информации о сериалах)

---

## Функционал
1. **Поиск сериалов**: Пользователь может искать сериалы по названию.
2. **Добавление в список**: Указать количество просмотренных сезонов/серий.
3. **Управление списком**: Просмотреть, удалить или изменить прогресс просмотров.
4. **Уведомления**: Получать уведомления о выходе новых серий.
5. **Статистика**: Просмотреть общее количество просмотренных сезонов/серий.

---

## Требования
- Python 3.9+
- Docker
- Docker Compose
- TMDb API ключ

---

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/series-tracker-bot.git
cd series-tracker-bot
```
### 2. Создание .env файла
Создайте файл .env в корне проекта и заполните его необходимыми данными:
```plaintext
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=series_tracker
POSTGRES_HOST=localhost

# API Keys
API_KEY_TMDB=your_tmdb_api_key

# Redis
REDIS_URL=redis://localhost:6379
```
Замените значения на свои данные:

your_telegram_bot_token: Токен вашего Telegram-бота.

your_password: Пароль для PostgreSQL.

your_tmdb_api_key: Ваш API-ключ для TMDb.

### 3. Запуск через Docker

Выполните следующую команду для сборки и запуска всех сервисов:
```bash
docker-compose up --build
```
Это:

Соберет Docker-образы для каждого микросервиса.

Запустит PostgreSQL, Redis, Telegram-бот, API-сервис и сервис уведомлений.
###  4. Применение миграций
```bash
docker exec -it series-tracker-bot_postgres_1 psql -U postgres -d series_tracker -f /path/to/migrations/001_initial.sql
```

Команды бота
<table>
<tr>
<td>/start</td>
<td>Начать работу с ботом</td>
</tr>
<tr>
<td>/add</td>
<td>Добавить сериал</td>
</tr>
<tr>
<td>/list</td>
<td>Просмотреть список сериалов</td>
</tr>
<tr>
<td>/notify</td>
<td>Настроить уведомления для конкретного сериала</td>
</tr>
<tr>
<td>/remove</td>
<td>Удалить сериал из списка</td>
</tr>
</table>

## Архитектура

Проект разделен на несколько микросервисов:

 - Telegram-бот (bot/) : Обработка команд пользователей.
 - API-сервис (api_service/) : Взаимодействие с внешними API (TMDb).
 - Уведомления (notifier/) : Периодическая проверка новых серий и отправка уведомлений.
 - PostgreSQL : Хранение данных пользователей и сериалов.
 - Redis : Кэширование данных API.
