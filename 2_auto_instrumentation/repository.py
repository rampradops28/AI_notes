"""
Repository Layer
================
Handles direct data persistence and retrieval from PostgreSQL using SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Query user by primary key ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Query user by unique email address."""
        return self.db.query(User).filter(User.email == email).first()

    def list_all(self) -> List[User]:
        """Retrieve all users from database."""
        return self.db.query(User).all()

    def create(self, name: str, email: str, role: str = "member") -> User:
        """Insert new user into database."""
        user = User(name=name, email=email, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
