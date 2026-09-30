"""
Database Configuration & Session Management
===========================================
Connects to PostgreSQL (running on localhost:5432) with automatic table creation
and seed data insertion.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

# Default to local PostgreSQL container on port 5433 (avoiding conflict with host port 5432)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/testdb"
)

try:
    engine = create_engine(DATABASE_URL, echo=False)
    # Test connection
    with engine.connect() as conn:
        pass
except Exception:
    # Graceful fallback to SQLite if PostgreSQL container is unreachable
    print("[Database] PostgreSQL connection failed, falling back to SQLite: test.db")
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create tables and seed initial demo users if empty."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            user1 = User(name="Alice Johnson", email="alice@example.com", role="admin")
            user2 = User(name="Bob Smith", email="bob@example.com", role="engineer")
            db.add_all([user1, user2])
            db.commit()
            print("[Database] Seeded 2 demo users into database.")
    finally:
        db.close()


def get_db():
    """FastAPI Dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
