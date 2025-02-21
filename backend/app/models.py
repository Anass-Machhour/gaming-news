from datetime import datetime, timezone
from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class Website(Base):
    __tablename__ = "websites"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(500), unique=True)
    favicon_url: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc))

    articles: Mapped[List["Article"]] = relationship(
        back_populates="website",
        cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Website(id={self.id!r}, url={self.url!r}, name={self.name!r}, favicon={self.favicon_url!r})"


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500), unique=True)
    headline: Mapped[str] = mapped_column(String(200))
    thumbnail_url: Mapped[str] = mapped_column(String(500))
    website_id: Mapped[int] = mapped_column(ForeignKey("websites.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc))

    website: Mapped["Website"] = relationship(back_populates="articles")

    def __repr__(self):
        return f"Article(id={self.id!r}, url={self.url!r}, headline={self.headline!r}, thumbnail={self.thumbnail!r})"
