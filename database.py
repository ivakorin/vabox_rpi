import sqlite3


class DataBase:
    def __init__(self, db_name=path.join(basedir, 'data.db')):
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()

    def install_tables(self):
        self.cursor.executescript('''CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY DEFAULT 1, last_news 
        TEXT, content TEXT, url TEXT); CREATE TABLE IF NOT EXISTS wall_posts(id INTEGER PRIMARY KEY AUTOINCREMENT NOT 
        NULL, post_id INTEGER); CREATE TABLE IF NOT EXISTS rules_requests(id INTEGER PRIMARY KEY AUTOINCREMENT NOT 
        NULL, last_post_date INTEGER, last_r_user_id INTEGER, message_id, INTEGER);
        ''')
        self.connect.commit()