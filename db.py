import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users WHERE tg_username=?', [str(user_id)]).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id, user_name):
        with self.connection:
            return self.cursor.execute('INSERT INTO users (tg_username, person_name, points, answered_questions_id) '
                                       'VALUES (?, ?, ?, ?)', (str(user_id), user_name, 0, -1))

    def get_points(self, user_id):
        with self.connection:
            result = \
                self.cursor.execute('SELECT points FROM users WHERE tg_username= \"' + str(user_id) + '\"').fetchone()[
                    0]
            return str(result)

    def get_name(self, user_id):
        with self.connection:
            return str(self.cursor.execute(
                'SELECT person_name FROM users WHERE tg_username = \"' + str(user_id) + '\"').fetchone()[0])
