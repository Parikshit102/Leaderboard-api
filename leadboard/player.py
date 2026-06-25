# models/player.py — Defines the Player table in the database

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Player(Base):
    __tablename__ = "players"

    id         = Column(Integer, primary_key=True, index=True)
    username   = Column(String, nullable=False)
    score      = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())  # auto timestamp
