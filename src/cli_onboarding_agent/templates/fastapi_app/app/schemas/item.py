"""
Item schemas for {{project_name}}.

This module defines Pydantic models for item data validation and serialization.
"""

from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    """Base item schema with common attributes."""

    title: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class ItemCreate(ItemBase):
    """Schema for creating a new item."""

    owner_id: int


class ItemUpdate(BaseModel):
    """Schema for updating an item."""

    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    owner_id: Optional[int] = None


class ItemResponse(ItemBase):
    """Schema for item response data."""

    id: int
    owner_id: int

    class Config:
        """Pydantic config."""

        orm_mode = True
