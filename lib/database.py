import asyncpg
import functools
from typing import List, Mapping


class Database:
    def __init__(self, url: str) -> None:
        self.url = url
        self.pool = None

    async def setup(self) -> asyncpg.Pool:
        self.pool = await asyncpg.create_pool(self.url)
        return self.pool

    def check_connection(func):
        @functools.wraps(func)
        async def inner(self, *args, **kwargs):
            self.pool = self.pool or self.setup()
            return await func(self, *args, **kwargs)
        return inner

    @check_connection
    async def execute(self, sql: str) -> None:
        async with self.pool.acquire() as con:
            await con.execute(sql)

    @check_connection
    async def fetch(self, sql: str) -> List[asyncpg.Record]:
        async with self.pool.acquire() as con:
            data = con.fetch(sql)
        return data

    # message count
    @check_connection
    async def get_count_map(self) -> Mapping[int, int]:
        async with self.pool.acquire() as con:
            data = con.fetch("SELECT * FROM count")
        count_map = {rec["user_id"]: rec["count"] for rec in data}
        return count_map

    @check_connection
    async def count_up(self, user_id: int, up_count: int = 1) -> None:
        async with self.pool.acquire() as con:
            await con.execute(f"UPDATE count SET count+={up_count} WHERE user_id={user_id}")

    @check_connection
    async def add_user(self, user_id: int) -> None:
        async with self.pool.acquire() as con:
            await con.execute(f"INSERT INTO count VALUES ({user_id}, 0)")

    @check_connection
    async def remove_user(self, user_id: int) -> None:
        async with self.pool.acquire() as con:
            await con.execute(f"DELETE FROM count WHERE user_id={user_id}")

    @check_connection
    async def reset_count(self) -> None:
        async with self.pool.acquire() as con:
            await con.execute("UPDATE count SET count=0")
