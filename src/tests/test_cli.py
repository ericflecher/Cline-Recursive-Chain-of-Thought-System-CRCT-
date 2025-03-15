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


@pytest.fixture
def temp_domains_dir(tmp_path):
    """Fixture for creating a temporary domains directory."""
    domains_dir = tmp_path / "domains"
    return domains_dir


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
            "--domains-dir", str(temp_target_dir.parent / "domains")
        ]
    )
    assert result.exit_code == 0
    
    # Check that the domains directory was created
    domains_dir = temp_target_dir.parent / "domains"
    assert domains_dir.exists()
    assert domains_dir.is_dir()
    
    # The project should be created in domains/target
    project_dir = domains_dir / temp_target_dir.name
    assert project_dir.exists()
    assert project_dir.is_dir()
    
    # Check that the expected directories were created
    assert (project_dir / "src").exists()
    assert (project_dir / "docs").exists()
    assert (project_dir / "tests").exists()
    
    # Check that the expected files were created
    assert (project_dir / "README.md").exists()
    assert (project_dir / "src" / "__init__.py").exists()
    assert (project_dir / "src" / "main.py").exists()
    assert (project_dir / "docs" / "README.md").exists()
    
    # Check that the guide document was excluded
    assert not (project_dir / "README_guide.md").exists()


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
            "--domains-dir", str(temp_target_dir.parent / "domains")
        ]
    )
    assert result.exit_code == 0
    
    # The project should be created in domains/target
    project_dir = temp_target_dir.parent / "domains" / temp_target_dir.name
    
    # Check that README.md was included despite the exclude pattern
    assert (project_dir / "README.md").exists()
    
    # Check that other .md files were excluded
    assert not (project_dir / "docs" / "README.md").exists()


def test_domains_directory_creation(runner, temp_template_dir, tmp_path):
    """Test that projects are created in the domains directory."""
    # Define a project name
    project_name = "test-project"
    
    # Define a domains directory
    domains_dir = tmp_path / "custom-domains"
    
    # Run the CLI with the domains-dir option
    result = runner.invoke(
        main,
        [
            project_name,
            "--domains-dir", str(domains_dir),
            "--template", str(temp_template_dir),
            "--force",
            "--verbose",
        ]
    )
    assert result.exit_code == 0
    
    # Check that the domains directory was created
    assert domains_dir.exists()
    assert domains_dir.is_dir()
    
    # Check that the project was created inside the domains directory
    project_path = domains_dir / project_name
    assert project_path.exists()
    assert project_path.is_dir()
    
    # Check that the expected directories were created inside the project
    assert (project_path / "src").exists()
    assert (project_path / "docs").exists()
    assert (project_path / "tests").exists()


def test_domains_directory_default(runner, temp_template_dir, tmp_path):
    """Test that projects are created in the default domains directory if not specified."""
    # Define a project name
    project_name = "test-project"
    
    # Run the CLI without specifying a domains directory (should use the default "domains")
    with runner.isolated_filesystem(temp_dir=tmp_path) as fs:
        result = runner.invoke(
            main,
            [
                project_name,
                "--template", str(temp_template_dir),
                "--force",
                "--verbose",
            ]
        )
        assert result.exit_code == 0
        
        # Check that the default domains directory was created
        domains_dir = Path(fs) / "domains"
        assert domains_dir.exists()
        assert domains_dir.is_dir()
        
        # Check that the project was created inside the domains directory
        project_path = domains_dir / project_name
        assert project_path.exists()
        assert project_path.is_dir()


def test_absolute_path_in_domains(runner, temp_template_dir, tmp_path):
    """Test that absolute paths are correctly placed in the domains directory."""
    # Define an absolute path for the project
    project_path = tmp_path / "absolute-path-project"
    
    # Define a domains directory
    domains_dir = tmp_path / "domains-for-absolute"
    
    # Run the CLI with an absolute path and domains-dir option
    result = runner.invoke(
        main,
        [
            str(project_path),
            "--domains-dir", str(domains_dir),
            "--template", str(temp_template_dir),
            "--force",
            "--verbose",
        ]
    )
    assert result.exit_code == 0
    
    # Check that the domains directory was created
    assert domains_dir.exists()
    assert domains_dir.is_dir()
    
    # Check that the project was created inside the domains directory with just the name
    expected_path = domains_dir / project_path.name
    assert expected_path.exists()
    assert expected_path.is_dir()
