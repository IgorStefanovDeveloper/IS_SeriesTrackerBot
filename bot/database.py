import psycopg2
from psycopg2.extras import DictCursor

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST", "localhost")
        )
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)

    def add_user(self, user_id, username):
        query = "INSERT INTO users (id, username) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING"
        self.cursor.execute(query, (user_id, username))
        self.conn.commit()

    def get_user(self, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def add_series(self, user_id, series_name, api_id, seasons_watched):
        # Добавляем сериал в таблицу series, если его нет
        self._add_series_to_db(series_name, api_id)

        # Получаем ID сериала
        series_id = self.get_series_id_by_api_id(api_id)

        # Добавляем связь между пользователем и сериалом
        query = """
        INSERT INTO user_series (user_id, series_id, seasons_watched)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, series_id) DO UPDATE SET seasons_watched = EXCLUDED.seasons_watched
        """
        self.cursor.execute(query, (user_id, series_id, seasons_watched))
        self.conn.commit()

    def _add_series_to_db(self, series_name, api_id):
        query = "INSERT INTO series (name, api_id) VALUES (%s, %s) ON CONFLICT (api_id) DO NOTHING"
        self.cursor.execute(query, (series_name, api_id))
        self.conn.commit()

    def get_series_id_by_api_id(self, api_id):
        query = "SELECT id FROM series WHERE api_id = %s"
        self.cursor.execute(query, (api_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_user_series(self, user_id):
        query = """
        SELECT s.name, us.seasons_watched, us.episodes_watched, us.notify
        FROM user_series us
        JOIN series s ON us.series_id = s.id
        WHERE us.user_id = %s
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def update_notify_flag(self, user_id, series_id, notify):
        query = "UPDATE user_series SET notify = %s WHERE user_id = %s AND series_id = %s"
        self.cursor.execute(query, (notify, user_id, series_id))
        self.conn.commit()
