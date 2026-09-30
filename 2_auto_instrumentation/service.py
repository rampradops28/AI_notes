"""
Service Layer
=============
Contains business logic, domain validation, and data orchestration.
Invokes UserRepository for data operations.
"""

from typing import List, Dict, Any
from repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Business Logic:
        1. Fetch user from repository.
        2. Validate existence.
        3. Format response.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist.")
        return user.to_dict()

    def create_user(self, name: str, email: str, role: str = "member") -> Dict[str, Any]:
        """
        Business Logic:
        1. Normalize email to lowercase.
        2. Check for duplicate registration.
        3. Validate role.
        4. Persist via repository.
        """
        clean_email = email.strip().lower()
        existing = self.repository.get_by_email(clean_email)
        if existing:
            raise ValueError(f"Email '{clean_email}' is already registered.")

        clean_name = name.strip()
        if not clean_name:
            raise ValueError("User name cannot be empty.")

        new_user = self.repository.create(name=clean_name, email=clean_email, role=role)
        return new_user.to_dict()

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Retrieve and format list of all users."""
        users = self.repository.list_all()
        return [u.to_dict() for u in users]
