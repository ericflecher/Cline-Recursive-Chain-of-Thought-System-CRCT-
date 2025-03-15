"""
UI utilities for the CLI Onboarding Agent.

This module provides utilities for enhancing the user interface of the CLI Onboarding Agent,
including color-coded output, progress bars, and interactive prompts.
"""

import sys
import logging
from typing import List, Dict, Any, Optional, Callable, Iterable, TypeVar, Union

import click
from tqdm import tqdm

# Type variables
T = TypeVar('T')

# Set up logging
logger = logging.getLogger("cli_onboarding_agent")


def print_success(message: str) -> None:
    """
    Print a success message in green.
    
    Args:
        message: The message to print
    """
    click.secho(message, fg="green")


def print_error(message: str) -> None:
    """
    Print an error message in red.
    
    Args:
        message: The message to print
    """
    click.secho(message, fg="red")


def print_warning(message: str) -> None:
    """
    Print a warning message in yellow.
    
    Args:
        message: The message to print
    """
    click.secho(message, fg="yellow")


def print_info(message: str) -> None:
    """
    Print an info message in blue.
    
    Args:
        message: The message to print
    """
    click.secho(message, fg="blue")


def print_header(message: str) -> None:
    """
    Print a header message in bold white.
    
    Args:
        message: The message to print
    """
    click.secho(message, fg="white", bold=True)


def print_step(step: int, total: int, message: str) -> None:
    """
    Print a step message with step number.
    
    Args:
        step: The current step number
        total: The total number of steps
        message: The message to print
    """
    click.secho(f"Step {step}/{total}: ", fg="blue", nl=False)
    click.echo(message)


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Confirm an action with the user.
    
    Args:
        message: The message to display
        default: The default value if the user just presses Enter
        
    Returns:
        True if the user confirmed, False otherwise
    """
    return click.confirm(message, default=default)


def select_option(message: str, options: List[str], default: Optional[int] = None) -> str:
    """
    Let the user select an option from a list.
    
    Args:
        message: The message to display
        options: The list of options to choose from
        default: The default option index if the user just presses Enter
        
    Returns:
        The selected option
    """
    return click.prompt(
        message,
        type=click.Choice(options),
        default=options[default] if default is not None else None,
        show_choices=True
    )


def progress_bar(
    iterable: Optional[Iterable[T]] = None,
    total: Optional[int] = None,
    desc: Optional[str] = None,
    unit: str = "it"
) -> Union[tqdm, Callable[[Iterable[T]], Iterable[T]]]:
    """
    Create a progress bar for an iterable or a total count.
    
    Args:
        iterable: The iterable to iterate over
        total: The total number of items
        desc: The description of the progress bar
        unit: The unit of the items
        
    Returns:
        A progress bar object or a decorator function
    """
    if iterable is not None:
        return tqdm(
            iterable,
            desc=desc,
            unit=unit,
            file=sys.stdout,
            dynamic_ncols=True
        )
    else:
        return tqdm(
            total=total,
            desc=desc,
            unit=unit,
            file=sys.stdout,
            dynamic_ncols=True
        )


def progress_callback(
    total: int,
    desc: str = "Processing",
    unit: str = "it"
) -> Callable[[int], None]:
    """
    Create a progress callback function for updating a progress bar.
    
    Args:
        total: The total number of items
        desc: The description of the progress bar
        unit: The unit of the items
        
    Returns:
        A callback function that updates the progress bar
    """
    progress = tqdm(total=total, desc=desc, unit=unit, file=sys.stdout, dynamic_ncols=True)
    
    def update(n: int = 1) -> None:
        progress.update(n)
        if progress.n >= total:
            progress.close()
    
    return update


def process_with_progress(
    items: List[T],
    process_func: Callable[[T], Any],
    desc: str = "Processing",
    unit: str = "it"
) -> List[Any]:
    """
    Process a list of items with a progress bar.
    
    Args:
        items: The list of items to process
        process_func: The function to process each item
        desc: The description of the progress bar
        unit: The unit of the items
        
    Returns:
        A list of processed items
    """
    results = []
    with progress_bar(total=len(items), desc=desc, unit=unit) as pbar:
        for item in items:
            result = process_func(item)
            results.append(result)
            pbar.update(1)
    return results


class LogFormatter(logging.Formatter):
    """
    Custom log formatter with color support.
    """
    
    COLORS = {
        logging.DEBUG: dict(fg="cyan"),
        logging.INFO: dict(fg="blue"),
        logging.WARNING: dict(fg="yellow"),
        logging.ERROR: dict(fg="red"),
        logging.CRITICAL: dict(fg="red", bold=True)
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record with color.
        
        Args:
            record: The log record to format
            
        Returns:
            The formatted log record
        """
        log_message = super().format(record)
        
        if not sys.stdout.isatty():
            return log_message
        
        color_kwargs = self.COLORS.get(record.levelno, {})
        return click.style(log_message, **color_kwargs)


def setup_colored_logging(logger_instance: logging.Logger) -> None:
    """
    Set up colored logging for a logger instance.
    
    Args:
        logger_instance: The logger instance to set up
    """
    for handler in logger_instance.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(LogFormatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))
