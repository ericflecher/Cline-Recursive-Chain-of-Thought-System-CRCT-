"""
User endpoints for {{project_name}}.

This module defines API endpoints for user management.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all users.

    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
        db: Database session

    Returns:
        List of users
    """
    service = UserService(db)
    users = service.get_users(skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user.

    Args:
        user: User data
        db: Database session

    Returns:
        Created user

    Raises:
        HTTPException: If a user with the same email already exists
    """
    service = UserService(db)
    
    # Check if user with the same email already exists
    existing_user = service.get_user_by_email(email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    return service.create_user(user=user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific user by ID.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        User data

    Raises:
        NotFoundException: If the user is not found
    """
    service = UserService(db)
    user = service.get_user(user_id=user_id)
    if not user:
        raise NotFoundException(detail=f"User with ID {user_id} not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a user.

    Args:
        user_id: User ID
        user: Updated user data
        db: Database session

    Returns:
        Updated user

    Raises:
        NotFoundException: If the user is not found
    """
    service = UserService(db)
    existing_user = service.get_user(user_id=user_id)
    if not existing_user:
        raise NotFoundException(detail=f"User with ID {user_id} not found")
    
    return service.update_user(user_id=user_id, user=user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a user.

    Args:
        user_id: User ID
        db: Database session

    Raises:
        NotFoundException: If the user is not found
    """
    service = UserService(db)
    existing_user = service.get_user(user_id=user_id)
    if not existing_user:
        raise NotFoundException(detail=f"User with ID {user_id} not found")
    
    service.delete_user(user_id=user_id)
