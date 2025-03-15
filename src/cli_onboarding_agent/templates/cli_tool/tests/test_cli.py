"""
Tests for the CLI tool.

This module contains tests for the CLI commands.
"""

import pytest
from click.testing import CliRunner

from {{package_name}}.cli import cli


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


def test_cli_help(runner):
    """Test the CLI help command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "{{description}}" in result.output


def test_hello_command(runner):
    """Test the hello command."""
    # Test without a name
    result = runner.invoke(cli, ["hello"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output

    # Test with a name
    result = runner.invoke(cli, ["hello", "Alice"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output


def test_echo_command(runner):
    """Test the echo command."""
    # Test with default count
    result = runner.invoke(cli, ["echo", "Hello"])
    assert result.exit_code == 0
    assert "Hello" in result.output
    assert result.output.count("Hello") == 1

    # Test with custom count
    result = runner.invoke(cli, ["echo", "-c", "3", "Hello"])
    assert result.exit_code == 0
    assert "Hello" in result.output
    assert result.output.count("Hello") == 3


def test_verbose_mode(runner):
    """Test the verbose mode."""
    # This test is a bit tricky since we can't easily check the log level
    # But we can at least make sure the command runs without errors
    result = runner.invoke(cli, ["-v", "hello"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output
