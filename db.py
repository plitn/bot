import sqlite3


# 1️⃣2️⃣3️⃣4️⃣

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users WHERE tg_username=?', [str(user_id)]).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO users (tg_username) VALUES (?)', str(user_id))

    def get_current_question_id(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT current_question FROM users WHERE tg_username = \"' +
                                       str(user_id) + '\"').fetchone()[0]

    def get_question_text(self, user_id):
        with self.connection:
            return self.cursor.execute(
                'SELECT text FROM questions WHERE id = ' + str(self.get_current_question_id(user_id))).fetchone()[0]

    def get_correct_answer_id(self, question_id):
        with self.connection:
            return self.cursor.execute('SELECT answer_id FROM questions WHERE id = ' + str(question_id)).fetchone()[0]

    def change_current_question_id(self, user_id):
        with self.connection:
            self.cursor.execute(
                'UPDATE users SET current_question = current_question + 1 WHERE tg_username = \"' + str(user_id) + '\"')

    def get_answer_reply(self, question_id):
        with self.connection:
            return self.cursor.execute('SELECT reply FROM questions WHERE id = ' + str(question_id)).fetchone()[0]

    def get_variants(self, question_id):
        with self.connection:
            if self.get_number_of_variants(question_id) == 4:
                return "1️⃣ " + str(
                    self.cursor.execute('SELECT answer1 FROM questions WHERE id = ' + str(question_id)).fetchone()[0]) \
                       + '\n2️⃣ ' + str(
                    self.cursor.execute('SELECT answer2 FROM questions WHERE id = ' + str(question_id)).fetchone()[0]) \
                       + '\n3️⃣ ' + str(
                    self.cursor.execute('SELECT answer3 FROM questions WHERE id = ' + str(question_id)).fetchone()[0]) \
                       + '\n4️⃣ ' + str(
                    self.cursor.execute('SELECT answer4 FROM questions WHERE id = ' + str(question_id)).fetchone()[0])
            elif self.get_number_of_variants(question_id) == 3:
                return "1️⃣ " + str(
                    self.cursor.execute('SELECT answer1 FROM questions WHERE id = ' + str(question_id)).fetchone()[0]) \
                       + '\n2️⃣ ' + str(
                    self.cursor.execute('SELECT answer2 FROM questions WHERE id = ' + str(question_id)).fetchone()[0]) \
                       + '\n3️⃣ ' + str(
                    self.cursor.execute('SELECT answer3 FROM questions WHERE id = ' + str(question_id)).fetchone()[0])
            elif self.get_number_of_variants(question_id) == 2:
                return "1️⃣ " + str(
                    self.cursor.execute('SELECT answer1 FROM questions WHERE id = ' + str(question_id)).fetchone()[0]) \
                       + '\n2️⃣ ' + str(
                    self.cursor.execute('SELECT answer2 FROM questions WHERE id = ' + str(question_id)).fetchone()[0])

    def get_number_of_variants(self, question_id):
        with self.connection:
            return self.cursor.execute('SELECT ans_quantity FROM questions WHERE id = ' + str(question_id)).fetchone()[
                0]

    def check_max_id(self):
        with self.connection:
            return self.cursor.execute('SELECT MAX(id) FROM questions').fetchone()[0]
