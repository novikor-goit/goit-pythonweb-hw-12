from datetime import datetime, date

from sqlalchemy import Integer, String, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.sql.sqltypes import DateTime, Date


class Base(DeclarativeBase): ...


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
