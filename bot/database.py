import psycopg2
import os

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST")
        )
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, username):
        self.cursor.execute("INSERT INTO users (id, username) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", (user_id, username))
        self.connection.commit()

    def add_user_series(self, user_id, series_name):
        self.cursor.execute("SELECT id FROM series WHERE name = %s", (series_name,))
        series_id = self.cursor.fetchone()
        if series_id:
            self.cursor.execute("INSERT INTO user_series (user_id, series_id) VALUES (%s, %s) ON CONFLICT (user_id, series_id) DO NOTHING", (user_id, series_id[0]))
            self.connection.commit()

    def update_user_series(self, user_id, series_name, seasons_watched, episodes_watched):
        self.cursor.execute("SELECT id FROM series WHERE name = %s", (series_name,))
        series_id = self.cursor.fetchone()
        if series_id:
            self.cursor.execute("UPDATE user_series SET seasons_watched = %s, episodes_watched = %s WHERE user_id = %s AND series_id = %s",
                                (seasons_watched, episodes_watched, user_id, series_id[0]))
            self.connection.commit()

    def update_notify(self, user_id, series_name, notify):
        self.cursor.execute("SELECT id FROM series WHERE name = %s", (series_name,))
        series_id = self.cursor.fetchone()
        if series_id:
            self.cursor.execute("UPDATE user_series SET notify = %s WHERE user_id = %s AND series_id = %s",
                                (notify, user_id, series_id[0]))
            self.connection.commit()
