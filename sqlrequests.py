# В этом файле будут функции для 

import aiosqlite

DB_PATH = "db.sqlite3"

async def create_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                tg_id TEXT,
                email TEXT
            )"""
        )
        await db.commit()
        await db.close()

async def get_column_names(table):
    async with aiosqlite.connect(DB_PATH) as db:
        some_sql = await db.execute(f"PRAGMA table_info('{table}')")
        column_names = [i[1] for i in await some_sql.fetchall()]
        await db.close()
        return column_names
        
    
async def insert_info(table, data):
    async with aiosqlite.connect(DB_PATH) as db:
        cols = await get_column_names(table)
        col_names = ', '.join(cols[1:])
        format_data = ', '.join([f"'{d}'" for d in data])
        some_sql = await db.execute(f"INSERT INTO {table} ({col_names}) VALUES ({format_data})")
        
        await db.commit()
        await db.close()

