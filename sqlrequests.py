# # В этом файле будут функции для 

import aiosqlite as sl
import asyncio

class DataBase:
    def __init__(self, path):
        self.path = path
        self.db = None  
        self.lock = asyncio.Lock()

    async def __aenter__(self):
        self.db = await sl.connect(self.path)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()

    async def drop_table(self, table):
        async with self.lock: 
            if not self.db:
                async with self:
                    await self.db.execute(f"DROP TABLE {table}")

# class DataBase:
#     async def create_table(self, table):
#         con = await Connection().connect()
#         async with con:
#                 some_sql = await con.execute(f"""CREATE TABLE IF NOT EXISTS {table} 
#                                     (id INTEGER PRIMARY KEY, 
#                                     user_tg INTEGER, 
#                                     user_email TEXT) """)  

#     async def get_col_names(self, table_name):
#         async with self.db as con:
#             some_sql = con.execute(f"PRAGMA table_info('{table_name}')")
#             column_names = [i[1] for i in some_sql.fetchall()]
#             return column_names

#     async def inster_info(self, table, data):
#         col_names = ', '.join(await self.get_col_names(table)[1:])
#         format_data = ', '.join([f"'{d}'" for d in data])
#         async with self.db as con:
#             some_sql = con.execute(f"INSERT INTO {table} ({col_names}) VALUES ({format_data})") 

#     # Функции разработчика(xd), не исаользуются в боте
#     async def get_table_names(self):
#         async with self.db as con:
#             some_sql = con.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
#         return some_sql.fetchall()
    
#     async def drop(self, table_name):
#         con = await Connection().connect()
#         async with con:
#             some_sql = await con.execute(f"DROP TABLE {table_name}")

db = DataBase('db.sqlite3')
