"""
Item endpoints for {{project_name}}.

This module defines API endpoints for item management.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.db.session import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter()


@router.get("/", response_model=List[ItemResponse])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all items.

    Args:
        skip: Number of items to skip
        limit: Maximum number of items to return
        db: Database session

    Returns:
        List of items
    """
    service = ItemService(db)
    items = service.get_items(skip=skip, limit=limit)
    return items


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new item.

    Args:
        item: Item data
        db: Database session

    Returns:
        Created item
    """
    service = ItemService(db)
    return service.create_item(item=item)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific item by ID.

    Args:
        item_id: Item ID
        db: Database session

    Returns:
        Item data

    Raises:
        NotFoundException: If the item is not found
    """
    service = ItemService(db)
    item = service.get_item(item_id=item_id)
    if not item:
        raise NotFoundException(detail=f"Item with ID {item_id} not found")
    return item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an item.

    Args:
        item_id: Item ID
        item: Updated item data
        db: Database session

    Returns:
        Updated item

    Raises:
        NotFoundException: If the item is not found
    """
    service = ItemService(db)
    existing_item = service.get_item(item_id=item_id)
    if not existing_item:
        raise NotFoundException(detail=f"Item with ID {item_id} not found")
    
    return service.update_item(item_id=item_id, item=item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an item.

    Args:
        item_id: Item ID
        db: Database session

    Raises:
        NotFoundException: If the item is not found
    """
    service = ItemService(db)
    existing_item = service.get_item(item_id=item_id)
    if not existing_item:
        raise NotFoundException(detail=f"Item with ID {item_id} not found")
    
    service.delete_item(item_id=item_id)
