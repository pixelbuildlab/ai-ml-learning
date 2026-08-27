import pathlib
import aiosqlite

current_path = pathlib.Path(__file__).parent.parent
DB_PATH = f"{current_path}/memory.sqlite"


async def get_connection():
    conn = await aiosqlite.connect(DB_PATH)
    conn.row_factory = aiosqlite.Row
    await conn.execute("PRAGMA foreign_keys = ON")
    return conn
