"""
Command-line interface for {{project_name}}.

This module provides the main entry point for the CLI tool.
"""

import logging
import sys
from typing import Optional

import click

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("{{package_name}}")


@click.group()
@click.version_option()
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Enable verbose output."
)
def cli(verbose: bool) -> None:
    """
    {{description}}
    
    Run '{{command_name}} COMMAND --help' for more information on a command.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")


@cli.command()
@click.argument("name", required=False)
def hello(name: Optional[str] = None) -> None:
    """
    Say hello to NAME or to the world if NAME is not provided.
    
    Examples:
        {{command_name}} hello
        {{command_name}} hello Alice
    """
    if name:
        click.echo(f"Hello, {name}!")
    else:
        click.echo("Hello, World!")
    logger.debug("Hello command executed")


@cli.command()
@click.option(
    "-c", "--count",
    type=int,
    default=1,
    help="Number of times to repeat the message."
)
@click.argument("message")
def echo(count: int, message: str) -> None:
    """
    Echo MESSAGE COUNT times.
    
    Examples:
        {{command_name}} echo "Hello"
        {{command_name}} echo -c 3 "Hello"
    """
    for _ in range(count):
        click.echo(message)
    logger.debug(f"Echo command executed with message: {message}, count: {count}")


if __name__ == "__main__":
    cli()  # pragma: no cover
