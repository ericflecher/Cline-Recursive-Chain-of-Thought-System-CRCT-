"""
User service for {{project_name}}.

This module provides services for user management.
"""

from typing import List, Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service for user management."""

    def __init__(self, db: Session):
        """Initialize the service with a database session.

        Args:
            db: Database session
        """
        self.db = db

    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID.

        Args:
            user_id: User ID

        Returns:
            User object or None if not found
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email.

        Args:
            email: User email

        Returns:
            User object or None if not found
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users.

        Args:
            skip: Number of users to skip
            limit: Maximum number of users to return

        Returns:
            List of users
        """
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate) -> User:
        """Create a new user.

        Args:
            user: User data

        Returns:
            Created user
        """
        hashed_password = self._get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user: UserUpdate) -> User:
        """Update a user.

        Args:
            user_id: User ID
            user: Updated user data

        Returns:
            Updated user
        """
        db_user = self.get_user(user_id)
        update_data = user.dict(exclude_unset=True)

        # Hash password if provided
        if "password" in update_data:
            update_data["hashed_password"] = self._get_password_hash(update_data.pop("password"))

        # Update user attributes
        for key, value in update_data.items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> None:
        """Delete a user.

        Args:
            user_id: User ID
        """
        db_user = self.get_user(user_id)
        self.db.delete(db_user)
        self.db.commit()

    def _get_password_hash(self, password: str) -> str:
        """Hash a password.

        Args:
            password: Plain password

        Returns:
            Hashed password
        """
        return pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password.

        Args:
            plain_password: Plain password
            hashed_password: Hashed password

        Returns:
            True if the password is correct, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)
