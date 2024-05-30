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
        await db.execute(
            """CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                tg_id TEXT,
                tg_username TEXT,
                message TEXT
            )
            """
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

async def is_tg_id(tg_id):
    async with aiosqlite.connect(DB_PATH) as db:
        some_sql = await db.execute(f"""SELECT tg_id FROM users WHERE tg_id = {tg_id}""")
        tg = await some_sql.fetchone()
        formated_result = {}
        if tg:
            some_sql = await db.execute(f"""SELECT users.channel, twitchers.twitch FROM users
                                            JOIN twitchers ON users.id = twitchers.user_id
                                            WHERE users.tg_id = {tg[0]}""")
            result = await some_sql.fetchall()
            
            for r in result:
                formated_result.update({r[0]: r[1]})    

        await  db.close()
        return tg, formated_result

async def get_tg_channels(tg_id):
    async with aiosqlite.connect(DB_PATH) as db:
        some_sql = await db.execute(f"""SELECT channel FROM users WHERE tg_id = '{tg_id}'""")
        result = await some_sql.fetchall()
        result = [r[0] for r in result]

        return result

async def delete_record(name):
    async with aiosqlite.connect(DB_PATH) as db:
        some_sql = await db.execute(f"SELECT id FROM users WHERE channel = '{name}'")
        ids = await some_sql.fetchall()
        if ids:
            ids = [i[0] for i in ids]
            for id in ids:
                some_sql = await db.execute(f"DELETE FROM twitchers WHERE user_id = '{id}'")
                some_sql = await db.execute(f"DELETE FROM users WHERE id = '{id}'")
            
            await db.commit()
            await db.close()
        else:
            return 'ids not found'


async def change_tg_channel(channel, tg_id):
    async with aiosqlite.connect(DB_PATH) as db:
        some_sql = await db.execute(f"UPDATE users SET channel = '{channel}' WHERE tg_id = '{tg_id}'")

        await db.commit()
        await db.close()

async def change_twitch_channel(channel, tg_id):
    async with aiosqlite.connect(DB_PATH) as db:
        some_sql = await db.execute(f"""UPDATE twitchers SET twitch = '{channel}'
                                        FROM users
                                        WHERE users.tg_id = '{tg_id}' AND twitchers.user_id = users.id""")
        
        await db.commit()
        await db.close()

async def get_feedback_table():
    async with aiosqlite.connect(DB_PATH) as db:
        formated_table = {}
        some_sql = await db.execute("""SELECT * FROM feedback""")
        table = await some_sql.fetchall()

        for t in table:
            if t[1] not in formated_table:
                formated_table[t[1]] = {'names': [t[2]], 'messages': [t[3]]} 
            else:
                if t[2] not in formated_table[t[1]]['names']:
                    formated_table[t[1]]['names'].append(t[2])
                formated_table[t[1]]['messages'].append(t[3])

        result = ''
        for t in formated_table:
            messages = "\n".join(formated_table[t]["messages"])
            result += f'Пользователь id {t} \nИменами {", ".join(formated_table[t]["names"])} \n' + \
            f'Отзывы: \n{messages}\n\n'
        
        await db.close()
        return result

async def drop_table(table):
    cols = await get_column_names(table)
    async with aiosqlite.connect(DB_PATH) as db:
        some_sql = await db.execute(f"DROP TABLE {table}")

        await db.close()


if __name__ == "__main__":
    asyncio.run(get_all_streamers())