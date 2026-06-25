# database.py — Sets up the database connection and session

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file — change to PostgreSQL URL in production
# Example PostgreSQL: "postgresql://user:password@localhost/leaderboard_db"
DATABASE_URL = "sqlite:///./leaderboard.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}   # needed only for SQLite
)

# Each request gets its own database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()


# ── Dependency — used in routers to get DB session ───────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db        # give session to the route
    finally:
        db.close()      # always close after request is done
