"""
Error handling module for the CLI Onboarding Agent.

This module provides centralized error handling functionality, including
custom exception classes, error logging, and decorators for consistent
error handling across the application.
"""

import logging
import traceback
import functools
from typing import Dict, Any, Optional, Callable, TypeVar, cast

logger = logging.getLogger("cli_onboarding_agent")

# Type variables for function decorators
F = TypeVar('F', bound=Callable[..., Any])
R = TypeVar('R')


class CLIError(Exception):
    """Base exception class for CLI Onboarding Agent errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """
        Initialize a CLI error.
        
        Args:
            message: The error message
            details: Additional details about the error
        """
        self.message = message
        self.details = details or {}
        super().__init__(message)
    
    def __str__(self) -> str:
        """Return a string representation of the error."""
        if self.details:
            return f"{self.message} (Details: {self.details})"
        return self.message


class TemplateError(CLIError):
    """Exception raised for errors related to templates."""
    pass


class GenerationError(CLIError):
    """Exception raised for errors during structure generation."""
    pass


class PopulationError(CLIError):
    """Exception raised for errors during document population."""
    pass


class ValidationError(CLIError):
    """Exception raised for validation errors."""
    pass


class AIAssistantError(CLIError):
    """Exception raised for errors related to the AI assistant."""
    pass


def handle_error(func: F) -> F:
    """
    Decorator for handling errors in CLI commands.
    
    This decorator catches exceptions, logs them appropriately,
    and returns an exit code.
    
    Args:
        func: The function to decorate
        
    Returns:
        The decorated function
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except CLIError as e:
            logger.error(f"CLI Error: {e.message}")
            for key, value in e.details.items():
                logger.error(f"  {key}: {value}")
            return 1
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return 1
    
    return cast(F, wrapper)


def log_exception(logger_instance: logging.Logger, level: int = logging.ERROR) -> Callable[[F], F]:
    """
    Decorator for logging exceptions without handling them.
    
    This decorator logs exceptions but allows them to propagate.
    
    Args:
        logger_instance: The logger to use
        level: The logging level to use
        
    Returns:
        A decorator function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger_instance.log(
                    level,
                    f"Exception in {func.__name__}: {str(e)}",
                    exc_info=True
                )
                raise
        
        return cast(F, wrapper)
    
    return decorator


def with_recovery(recovery_func: Callable[[Exception], R]) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """
    Decorator for adding recovery behavior to functions.
    
    This decorator catches exceptions and calls a recovery function.
    
    Args:
        recovery_func: A function that takes an exception and returns a recovery value
        
    Returns:
        A decorator function
    """
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Recovering from error in {func.__name__}: {str(e)}")
                return recovery_func(e)
        
        return wrapper
    
    return decorator
