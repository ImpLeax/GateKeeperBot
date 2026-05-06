import datetime
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from sqlalchemy.sql import func

from .models import BotUsers, Base

class BotDatabase:
    def __init__(self):
        self.user=os.getenv("POSTGRES_USER")
        self.password=os.getenv("POSTGRES_PASSWORD")
        self.host=os.getenv("POSTGRES_HOST")
        self.name=os.getenv("POSTGRES_DB")
        self.url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:5432/{self.name}"
        self.engine=create_async_engine(
            url=self.url,
            echo=False
        )
        self.session_factory=async_sessionmaker(self.engine)

    async def init_models(self):
        async with self.engine.begin() as conn: #type: ignore
            await conn.run_sync(Base.metadata.create_all)

    async def add_user(self, telegram_id, channel_id, username, first_name):
        async with self.session_factory() as session:
            user = BotUsers(tg_id=telegram_id, channel_id=channel_id, username=username, first_name=first_name)
            session.add(user)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()

    async def get_users(self):
        async with self.session_factory() as session:
            res = await session.execute(
                select(BotUsers.tg_id)
            )
            return res.scalars().all()

    async def delete_user(self, tg_id):
        async with self.session_factory() as session:
            await session.execute(
                delete(BotUsers).where(BotUsers.tg_id == tg_id)
            )
            await session.commit()

    async def get_stats(self):
        async with self.session_factory() as session:
            stats = dict()

            today_start = datetime.datetime.now(datetime.UTC).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

            query = select(
                func.count(BotUsers.id).label("total"),
                func.count().filter(BotUsers.created_at >= today_start).label("today")
            )
            res = await session.execute(query)
            res = res.all()
            stats["user_count"] = res[0][0]
            stats["users_today"] = res[0][1]

            return stats