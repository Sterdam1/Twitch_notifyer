# В этом файле будут функции для 
import sqlite3 as sl

# db = sl.connect('db.sqlite3', check_same_thread=False)

class DataBase:
    def __init__(self):
        # Надо ли подключание в самом классе или не надо?
        self.db = sl.connect('db.sqlite3')
        
        # user_email надо расширить до нескольких email'ов(приоритет 1)
        # Надо добавить ban list отправителей, чтобы не приходили емэйлы от каких-то людей,
        # или конкретно письма от конкретного получателя уведомлялись
        with self.db as con:
            some_sql = con.execute("""CREATE TABLE IF NOT EXISTS user_table 
                                   (id INTEGER PRIMARY KEY, 
                                   user_tg INTEGER, 
                                   user_email TEXT) """)
            
    def get_table_names(self):
        with self.db as con:
            some_sql = con.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
        return some_sql.fetchall()
    
db = DataBase()
print(db.get_table_names())
