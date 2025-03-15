"""
Tests for the error_handling module.
"""

import logging
import pytest
from unittest.mock import patch, MagicMock

from cli_onboarding_agent.error_handling import (
    CLIError, TemplateError, GenerationError, PopulationError, ValidationError, AIAssistantError,
    handle_error, log_exception, with_recovery
)


def test_cli_error_init():
    """Test initializing a CLIError."""
    error = CLIError("Test error")
    assert error.message == "Test error"
    assert error.details == {}
    
    error_with_details = CLIError("Test error", {"key": "value"})
    assert error_with_details.message == "Test error"
    assert error_with_details.details == {"key": "value"}


def test_cli_error_str():
    """Test the string representation of a CLIError."""
    error = CLIError("Test error")
    assert str(error) == "Test error"
    
    error_with_details = CLIError("Test error", {"key": "value"})
    assert str(error_with_details) == "Test error (Details: {'key': 'value'})"


def test_template_error():
    """Test the TemplateError class."""
    error = TemplateError("Template error", {"template": "test.py"})
    assert isinstance(error, CLIError)
    assert error.message == "Template error"
    assert error.details == {"template": "test.py"}


def test_generation_error():
    """Test the GenerationError class."""
    error = GenerationError("Generation error", {"file": "test.py"})
    assert isinstance(error, CLIError)
    assert error.message == "Generation error"
    assert error.details == {"file": "test.py"}


def test_population_error():
    """Test the PopulationError class."""
    error = PopulationError("Population error", {"file": "test.py"})
    assert isinstance(error, CLIError)
    assert error.message == "Population error"
    assert error.details == {"file": "test.py"}


def test_validation_error():
    """Test the ValidationError class."""
    error = ValidationError("Validation error", {"file": "test.py"})
    assert isinstance(error, CLIError)
    assert error.message == "Validation error"
    assert error.details == {"file": "test.py"}


def test_ai_assistant_error():
    """Test the AIAssistantError class."""
    error = AIAssistantError("AI error", {"model": "gpt-4"})
    assert isinstance(error, CLIError)
    assert error.message == "AI error"
    assert error.details == {"model": "gpt-4"}


def test_handle_error_decorator_with_cli_error():
    """Test the handle_error decorator with a CLIError."""
    logger = MagicMock()
    
    with patch("cli_onboarding_agent.error_handling.logger", logger):
        @handle_error
        def func_with_cli_error():
            raise CLIError("CLI error", {"key": "value"})
        
        result = func_with_cli_error()
        
        assert result == 1
        # Check that the error message was logged
        logger.error.assert_any_call("CLI Error: CLI error")


def test_handle_error_decorator_with_generic_error():
    """Test the handle_error decorator with a generic error."""
    logger = MagicMock()
    
    with patch("cli_onboarding_agent.error_handling.logger", logger):
        @handle_error
        def func_with_generic_error():
            raise ValueError("Generic error")
        
        result = func_with_generic_error()
        
        assert result == 1
        logger.error.assert_called_with("Unexpected error: Generic error")


def test_handle_error_decorator_with_success():
    """Test the handle_error decorator with a successful function."""
    @handle_error
    def func_success():
        return "success"
    
    result = func_success()
    assert result == "success"


def test_log_exception_decorator():
    """Test the log_exception decorator."""
    logger = MagicMock()
    
    @log_exception(logger)
    def func_with_error():
        raise ValueError("Test error")
    
    # The function should raise the error
    with pytest.raises(ValueError):
        func_with_error()
    
    # But it should also log the error
    logger.log.assert_called_once()
    args, kwargs = logger.log.call_args
    assert args[0] == logging.ERROR
    assert "Test error" in args[1]
    assert kwargs["exc_info"] is True


def test_with_recovery_decorator():
    """Test the with_recovery decorator."""
    def recovery_func(e):
        return f"Recovered from {str(e)}"
    
    @with_recovery(recovery_func)
    def func_with_error():
        raise ValueError("Test error")
    
    result = func_with_error()
    assert result == "Recovered from Test error"


def test_with_recovery_decorator_no_error():
    """Test the with_recovery decorator when no error occurs."""
    def recovery_func(e):
        return f"Recovered from {str(e)}"
    
    @with_recovery(recovery_func)
    def func_no_error():
        return "success"
    
    result = func_no_error()
    assert result == "success"
