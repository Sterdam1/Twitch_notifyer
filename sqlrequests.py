# В этом файле будут функции для 
import sqlite3 as sl

# db = sl.connect('db.sqlite3', check_same_thread=False)

class DataBase:
    def __init__(self):
        self.db = sl.connect('db.sqlite3')
        
        with self.db as con:
            some_sql = con.execute("""CREATE TABLE IF NOT EXISTS user_table 
                                   (id INTEGER PRIMARY KEY, user_tg INTEGER, user_email TEXT) """)
            
    def if_table(self):
        with self.db as con:
            some_sql = con.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
        return some_sql.fetchall()
    
db = DataBase()
print(db.if_table())
