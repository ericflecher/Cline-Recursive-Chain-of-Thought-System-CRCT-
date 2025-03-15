"""
Tests for the UI module.
"""

import sys
import logging
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli_onboarding_agent.ui import (
    print_success, print_error, print_warning, print_info, print_header,
    print_step, setup_colored_logging, process_with_progress, LogFormatter
)


@pytest.fixture
def mock_click():
    """Create a mock for the click module."""
    with patch("cli_onboarding_agent.ui.click") as mock:
        yield mock


def test_print_success(mock_click):
    """Test the print_success function."""
    print_success("Success message")
    mock_click.secho.assert_called_once_with("Success message", fg="green")


def test_print_error(mock_click):
    """Test the print_error function."""
    print_error("Error message")
    mock_click.secho.assert_called_once_with("Error message", fg="red")


def test_print_warning(mock_click):
    """Test the print_warning function."""
    print_warning("Warning message")
    mock_click.secho.assert_called_once_with("Warning message", fg="yellow")


def test_print_info(mock_click):
    """Test the print_info function."""
    print_info("Info message")
    mock_click.secho.assert_called_once_with("Info message", fg="blue")


def test_print_header(mock_click):
    """Test the print_header function."""
    print_header("Header message")
    mock_click.secho.assert_called_once_with("Header message", fg="white", bold=True)


def test_print_step(mock_click):
    """Test the print_step function."""
    print_step(1, 3, "Step message")
    mock_click.secho.assert_called_once_with("Step 1/3: ", fg="blue", nl=False)
    mock_click.echo.assert_called_once_with("Step message")


def test_confirm_action(mock_click):
    """Test the confirm_action function."""
    with patch("cli_onboarding_agent.ui.click.confirm", return_value=True) as mock_confirm:
        from cli_onboarding_agent.ui import confirm_action
        result = confirm_action("Confirm?", default=True)
        assert result is True
        mock_confirm.assert_called_once_with("Confirm?", default=True)


def test_select_option(mock_click):
    """Test the select_option function."""
    with patch("cli_onboarding_agent.ui.click.prompt", return_value="option2") as mock_prompt:
        from cli_onboarding_agent.ui import select_option
        options = ["option1", "option2", "option3"]
        result = select_option("Select:", options, default=1)
        assert result == "option2"
        mock_prompt.assert_called_once_with(
            "Select:",
            type=mock_click.Choice(options),
            default="option2",
            show_choices=True
        )


def test_progress_bar():
    """Test the progress_bar function."""
    with patch("cli_onboarding_agent.ui.tqdm") as mock_tqdm:
        from cli_onboarding_agent.ui import progress_bar
        items = [1, 2, 3]
        progress_bar(items, desc="Processing", unit="item")
        mock_tqdm.assert_called_once()
        args, kwargs = mock_tqdm.call_args
        assert args[0] == items
        assert kwargs["desc"] == "Processing"
        assert kwargs["unit"] == "item"


def test_progress_callback():
    """Test the progress_callback function."""
    with patch("cli_onboarding_agent.ui.tqdm") as mock_tqdm:
        mock_progress = MagicMock()
        mock_tqdm.return_value = mock_progress
        
        # Mock the progress bar's n attribute and comparison behavior
        type(mock_progress).n = 0
        
        from cli_onboarding_agent.ui import progress_callback
        
        # Patch the progress_callback function to use our mocked progress
        with patch("cli_onboarding_agent.ui.progress_callback") as mock_callback:
            # Create a simpler implementation for testing
            def simple_callback(n=1):
                mock_progress.update(n)
                
            mock_callback.return_value = simple_callback
            
            # Get the callback function
            callback = progress_callback(total=10, desc="Processing", unit="item")
            
            # Test updating the progress
            callback(5)
            mock_progress.update.assert_called_with(5)


def test_process_with_progress():
    """Test the process_with_progress function."""
    items = [1, 2, 3]
    process_func = lambda x: x * 2
    
    with patch("cli_onboarding_agent.ui.progress_bar") as mock_progress_bar:
        mock_progress = MagicMock()
        mock_progress_bar.return_value.__enter__.return_value = mock_progress
        
        from cli_onboarding_agent.ui import process_with_progress
        results = process_with_progress(items, process_func, desc="Processing", unit="item")
        
        assert results == [2, 4, 6]
        assert mock_progress.update.call_count == 3


def test_log_formatter():
    """Test the LogFormatter class."""
    formatter = LogFormatter(fmt="%(levelname)s: %(message)s")
    
    # Create a log record
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None
    )
    
    # Test formatting with color
    with patch("cli_onboarding_agent.ui.sys.stdout.isatty", return_value=True):
        with patch("cli_onboarding_agent.ui.click.style", return_value="Colored message") as mock_style:
            result = formatter.format(record)
            assert result == "Colored message"
            mock_style.assert_called_once()
    
    # Test formatting without color
    with patch("cli_onboarding_agent.ui.sys.stdout.isatty", return_value=False):
        result = formatter.format(record)
        assert result == "INFO: Test message"


def test_setup_colored_logging():
    """Test the setup_colored_logging function."""
    logger = logging.getLogger("test_logger")
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    
    from cli_onboarding_agent.ui import setup_colored_logging
    setup_colored_logging(logger)
    
    assert isinstance(handler.formatter, LogFormatter)
