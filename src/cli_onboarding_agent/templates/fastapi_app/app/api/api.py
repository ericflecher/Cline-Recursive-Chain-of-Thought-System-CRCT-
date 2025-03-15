"""
API router for {{project_name}}.

This module includes all API endpoints from different routers.
"""

from fastapi import APIRouter

from app.api.endpoints import items, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
