import datetime

from sqlalchemy import BigInteger, String, text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(
    DateTime(timezone=True),
    server_default=func.now()
)]
updated_at = Annotated[datetime.datetime, mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now()
)]

class Base(DeclarativeBase):
    pass

class BotUsers(Base):
    __tablename__ = "botusers"

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(64), nullable=True)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
