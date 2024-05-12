# В этом файле будут функции для 

import aiosqlite
import asyncio

DB_PATH = "db.sqlite3"

async def create_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                tg_id TEXT,
                channel TEXT
            )"""
        )
        await db.execute(
            """CREATE TABLE IF NOT EXISTS twitchers (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                twitch TEXT
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

async def get_col_by_col(table, col, filter, value):
    async with aiosqlite.connect(DB_PATH) as db:
        some_sql = await db.execute(f"SELECT {col} FROM {table} WHERE {filter} = {value}")  
        result = await some_sql.fetchall()
        await db.close()
        if result:
            return result[0][0]
        else: 
            return None
    
async def insert_info(table, data):
    async with aiosqlite.connect(DB_PATH) as db:
        cols = await get_column_names(table)
        col_names = ', '.join(cols[1:])
        format_data = ', '.join([f"'{d}'" for d in data])
        some_sql = await db.execute(f"INSERT INTO {table} ({col_names}) VALUES ({format_data})")
        
        await db.commit()
        await db.close()

async def get_all_streamers():
    async with aiosqlite.connect(DB_PATH) as db:
        some_sql = await db.execute("""SELECT twitchers.twitch, users.channel FROM twitchers
                                        JOIN users ON users.id = twitchers.user_id """)
        result = await some_sql.fetchall()
        await db.close()

        return result

async def drop_table(table):
    async with aiosqlite.connect(DB_PATH) as db:
        some_sql = await db.execute(f"DROP TABLE {table}")

        await db.close()


if __name__ == "__main__":
    asyncio.run(get_all_streamers())