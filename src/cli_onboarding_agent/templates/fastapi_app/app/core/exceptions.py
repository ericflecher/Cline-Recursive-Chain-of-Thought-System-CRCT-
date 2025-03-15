"""
Exception classes for {{project_name}}.

This module defines custom exception classes for the application.
"""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Base exception class for application-specific exceptions."""

    def __init__(
        self,
        detail: str,
        code: str = "error",
        status_code: int = 500,
        data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the exception.

        Args:
            detail: A human-readable error message
            code: A machine-readable error code
            status_code: The HTTP status code to return
            data: Additional data to include in the error response
        """
        self.detail = detail
        self.code = code
        self.status_code = status_code
        self.data = data or {}
        super().__init__(self.detail)


class NotFoundException(AppException):
    """Exception raised when a resource is not found."""

    def __init__(
        self,
        detail: str = "Resource not found",
        code: str = "not_found",
        data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the exception.

        Args:
            detail: A human-readable error message
            code: A machine-readable error code
            data: Additional data to include in the error response
        """
        super().__init__(detail=detail, code=code, status_code=404, data=data)


class ValidationException(AppException):
    """Exception raised when validation fails."""

    def __init__(
        self,
        detail: str = "Validation error",
        code: str = "validation_error",
        data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the exception.

        Args:
            detail: A human-readable error message
            code: A machine-readable error code
            data: Additional data to include in the error response
        """
        super().__init__(detail=detail, code=code, status_code=422, data=data)


class AuthenticationException(AppException):
    """Exception raised when authentication fails."""

    def __init__(
        self,
        detail: str = "Authentication failed",
        code: str = "authentication_error",
        data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the exception.

        Args:
            detail: A human-readable error message
            code: A machine-readable error code
            data: Additional data to include in the error response
        """
        super().__init__(detail=detail, code=code, status_code=401, data=data)


class AuthorizationException(AppException):
    """Exception raised when authorization fails."""

    def __init__(
        self,
        detail: str = "Not authorized",
        code: str = "authorization_error",
        data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the exception.

        Args:
            detail: A human-readable error message
            code: A machine-readable error code
            data: Additional data to include in the error response
        """
        super().__init__(detail=detail, code=code, status_code=403, data=data)
