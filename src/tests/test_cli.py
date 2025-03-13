"""
Tests for the CLI module.
"""

import os
import sys
import pytest
from pathlib import Path
from click.testing import CliRunner

from cli_onboarding_agent.cli import main


@pytest.fixture
def runner():
    """Fixture for creating a Click CLI runner."""
    return CliRunner()


@pytest.fixture
def temp_template_dir(tmp_path):
    """Fixture for creating a temporary template directory."""
    # Create a simple template structure
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    
    # Create some directories
    (template_dir / "src").mkdir()
    (template_dir / "docs").mkdir()
    (template_dir / "tests").mkdir()
    
    # Create some files
    (template_dir / "README.md").write_text("# Test Project")
    (template_dir / "src" / "__init__.py").write_text("")
    (template_dir / "src" / "main.py").write_text("print('Hello, world!')")
    (template_dir / "docs" / "README.md").write_text("# Documentation")
    
    # Create a guide document that should be excluded
    (template_dir / "README_guide.md").write_text("# Guide Document")
    
    return template_dir


@pytest.fixture
def temp_target_dir(tmp_path):
    """Fixture for creating a temporary target directory."""
    target_dir = tmp_path / "target"
    return target_dir


def test_cli_help(runner):
    """Test the CLI help output."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Generate a standardized folder structure from a template." in result.output


def test_cli_version(runner):
    """Test the CLI version output."""
    # Note: This assumes the CLI has a --version option, which it doesn't currently have
    # This test is included as an example and would need to be modified or removed
    # result = runner.invoke(main, ["--version"])
    # assert result.exit_code == 0
    # assert "cli_onboarding_agent" in result.output
    pass


def test_cli_dry_run(runner, temp_template_dir, temp_target_dir):
    """Test the CLI dry run mode."""
    # The output is being logged, not printed to stdout, so we can't check result.output
    # Instead, we'll just check that the command runs successfully and the target directory
    # is not created
    result = runner.invoke(
        main,
        [
            str(temp_target_dir),
            "--template", str(temp_template_dir),
            "--dry-run",
            "--verbose",
        ]
    )
    assert result.exit_code == 0
    
    # Target directory should not have been created in dry run mode
    assert not temp_target_dir.exists()


def test_cli_basic_generation(runner, temp_template_dir, temp_target_dir):
    """Test basic project generation."""
    # The output is being logged, not printed to stdout, so we can't check result.output
    result = runner.invoke(
        main,
        [
            str(temp_target_dir),
            "--template", str(temp_template_dir),
            "--force",
            "--verbose",
        ]
    )
    assert result.exit_code == 0
    
    # Check that the target directory was created
    assert temp_target_dir.exists()
    assert temp_target_dir.is_dir()
    
    # Check that the expected directories were created
    assert (temp_target_dir / "src").exists()
    assert (temp_target_dir / "docs").exists()
    assert (temp_target_dir / "tests").exists()
    
    # Check that the expected files were created
    assert (temp_target_dir / "README.md").exists()
    assert (temp_target_dir / "src" / "__init__.py").exists()
    assert (temp_target_dir / "src" / "main.py").exists()
    assert (temp_target_dir / "docs" / "README.md").exists()
    
    # Check that the guide document was excluded
    assert not (temp_target_dir / "README_guide.md").exists()


def test_cli_exclude_include(runner, temp_template_dir, temp_target_dir):
    """Test exclude and include patterns."""
    result = runner.invoke(
        main,
        [
            str(temp_target_dir),
            "--template", str(temp_template_dir),
            "--force",
            "--exclude", "*.md",
            "--include", "README.md",
            "--verbose",
        ]
    )
    assert result.exit_code == 0
    
    # Check that README.md was included despite the exclude pattern
    assert (temp_target_dir / "README.md").exists()
    
    # Check that other .md files were excluded
    assert not (temp_target_dir / "docs" / "README.md").exists()
