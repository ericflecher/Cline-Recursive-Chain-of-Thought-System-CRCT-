"""
Item service for {{project_name}}.

This module provides services for item management.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """Service for item management."""

    def __init__(self, db: Session):
        """Initialize the service with a database session.

        Args:
            db: Database session
        """
        self.db = db

    def get_item(self, item_id: int) -> Optional[Item]:
        """Get an item by ID.

        Args:
            item_id: Item ID

        Returns:
            Item object or None if not found
        """
        return self.db.query(Item).filter(Item.id == item_id).first()

    def get_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """Get all items.

        Args:
            skip: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of items
        """
        return self.db.query(Item).offset(skip).limit(limit).all()

    def get_user_items(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        """Get items for a specific user.

        Args:
            user_id: User ID
            skip: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of items
        """
        return (
            self.db.query(Item)
            .filter(Item.owner_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_item(self, item: ItemCreate) -> Item:
        """Create a new item.

        Args:
            item: Item data

        Returns:
            Created item
        """
        db_item = Item(
            title=item.title,
            description=item.description,
            is_active=item.is_active,
            owner_id=item.owner_id,
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update_item(self, item_id: int, item: ItemUpdate) -> Item:
        """Update an item.

        Args:
            item_id: Item ID
            item: Updated item data

        Returns:
            Updated item
        """
        db_item = self.get_item(item_id)
        update_data = item.dict(exclude_unset=True)

        # Update item attributes
        for key, value in update_data.items():
            setattr(db_item, key, value)

        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete_item(self, item_id: int) -> None:
        """Delete an item.

        Args:
            item_id: Item ID
        """
        db_item = self.get_item(item_id)
        self.db.delete(db_item)
        self.db.commit()
