"""
Item model for {{project_name}}.

This module defines the SQLAlchemy model for items.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Item(Base):
    """Item model."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Define relationships
    owner = relationship("User", back_populates="items")

    def __repr__(self):
        """Return string representation of the item."""
        return f"<Item(id={self.id}, title={self.title}, owner_id={self.owner_id})>"
