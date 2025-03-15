"""
User model for {{project_name}}.

This module defines the SQLAlchemy model for users.
"""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Define relationships
    items = relationship("Item", back_populates="owner")

    def __repr__(self):
        """Return string representation of the user."""
        return f"<User(id={self.id}, email={self.email}, full_name={self.full_name})>"
