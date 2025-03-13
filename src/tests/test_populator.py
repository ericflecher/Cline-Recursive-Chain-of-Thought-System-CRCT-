"""
Tests for the populator module.
"""

import os
import pytest
from pathlib import Path

from cli_onboarding_agent.template_reader import TemplateStructure, read_template
from cli_onboarding_agent.generator import generate_structure
from cli_onboarding_agent.populator import (
    populate_documents,
    copy_file,
    process_file_content,
    should_overwrite_file,
    validate_population,
    PopulationError
)


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
    
    # Create a file with template variables
    (template_dir / "config.txt").write_text("Project: {{ project_name }}\nVersion: {{ version }}")
    
    # Create a guide document that should be excluded
    (template_dir / "README_guide.md").write_text("# Guide Document")
    
    return template_dir


@pytest.fixture
def temp_target_dir(tmp_path):
    """Fixture for creating a temporary target directory."""
    target_dir = tmp_path / "target"
    target_dir.mkdir()
    return target_dir


@pytest.fixture
def template_structure(temp_template_dir):
    """Fixture for creating a template structure."""
    return read_template(temp_template_dir)


@pytest.fixture
def prepared_target_dir(temp_target_dir, temp_template_dir, template_structure):
    """Fixture for creating a target directory with the folder structure."""
    generate_structure(
        temp_target_dir,
        template_structure,
        temp_template_dir,
        dry_run=False,
        force=False
    )
    return temp_target_dir


def test_should_overwrite_file(temp_target_dir):
    """Test the should_overwrite_file function."""
    # Create a test file
    test_file = temp_target_dir / "test.txt"
    
    # Test with non-existent file
    assert should_overwrite_file(test_file) is True
    
    # Create the file
    test_file.write_text("test")
    
    # Test with existing file without force
    assert should_overwrite_file(test_file, force=False) is False
    
    # Test with existing file with force
    assert should_overwrite_file(test_file, force=True) is True


def test_copy_file(temp_template_dir, temp_target_dir):
    """Test the copy_file function."""
    source_file = temp_template_dir / "README.md"
    target_file = temp_target_dir / "README.md"
    
    # Test copying a file
    result = copy_file(source_file, target_file)
    assert result is True
    assert target_file.exists()
    assert target_file.read_text() == source_file.read_text()
    
    # Test copying to an existing file without force
    modified_content = "Modified content"
    target_file.write_text(modified_content)
    
    result = copy_file(source_file, target_file, force=False)
    assert result is False
    assert target_file.read_text() == modified_content  # Content should not change
    
    # Test copying to an existing file with force
    result = copy_file(source_file, target_file, force=True)
    assert result is True
    assert target_file.read_text() == source_file.read_text()  # Content should be overwritten
    
    # Test with dry run
    dry_run_file = temp_target_dir / "dry_run.txt"
    result = copy_file(source_file, dry_run_file, dry_run=True)
    assert result is True
    assert not dry_run_file.exists()


def test_process_file_content(temp_template_dir, temp_target_dir):
    """Test the process_file_content function."""
    source_file = temp_template_dir / "config.txt"
    target_file = temp_target_dir / "config.txt"
    
    # Copy the file first
    copy_file(source_file, target_file)
    
    # Test processing file content with variables
    variables = {
        "project_name": "Test Project",
        "version": "1.0.0"
    }
    
    result = process_file_content(source_file, target_file, variables)
    assert result is True
    
    # Check that variables were replaced
    content = target_file.read_text()
    assert "Project: Test Project" in content
    assert "Version: 1.0.0" in content
    
    # Test with no variables
    result = process_file_content(source_file, target_file)
    assert result is True


def test_populate_documents(temp_template_dir, prepared_target_dir, template_structure):
    """Test the populate_documents function."""
    # Populate documents
    stats = populate_documents(
        prepared_target_dir,
        temp_template_dir,
        template_structure,
        dry_run=False,
        force=False
    )
    
    # Check that files were copied
    assert (prepared_target_dir / "README.md").exists()
    assert (prepared_target_dir / "src" / "__init__.py").exists()
    assert (prepared_target_dir / "src" / "main.py").exists()
    assert (prepared_target_dir / "docs" / "README.md").exists()
    
    # Check that guide documents were excluded
    assert not (prepared_target_dir / "README_guide.md").exists()
    
    # Check the statistics
    assert stats["files_copied"] >= 5  # README.md, __init__.py, main.py, docs/README.md, config.txt
    assert stats["files_failed"] == 0
    
    # Test with variables
    variables = {
        "project_name": "Test Project",
        "version": "1.0.0"
    }
    
    stats = populate_documents(
        prepared_target_dir,
        temp_template_dir,
        template_structure,
        dry_run=False,
        force=True,
        variables=variables
    )
    
    # Check that variables were replaced
    config_content = (prepared_target_dir / "config.txt").read_text()
    assert "Project: Test Project" in config_content
    assert "Version: 1.0.0" in config_content
    
    # Test with dry run
    dry_run_dir = prepared_target_dir.parent / "dry_run"
    dry_run_dir.mkdir()
    
    stats = populate_documents(
        dry_run_dir,
        temp_template_dir,
        template_structure,
        dry_run=True,
        force=False
    )
    
    # Check that no files were copied
    assert not (dry_run_dir / "README.md").exists()


def test_validate_population(temp_template_dir, prepared_target_dir, template_structure):
    """Test the validate_population function."""
    # Populate documents
    populate_documents(
        prepared_target_dir,
        temp_template_dir,
        template_structure,
        dry_run=False,
        force=False
    )
    
    # Validate population
    is_valid, errors = validate_population(
        prepared_target_dir,
        template_structure,
        temp_template_dir
    )
    
    assert is_valid is True
    assert len(errors) == 0
    
    # Remove a file and validate again
    (prepared_target_dir / "README.md").unlink()
    
    is_valid, errors = validate_population(
        prepared_target_dir,
        template_structure,
        temp_template_dir
    )
    
    assert is_valid is False
    assert len(errors) == 1
    assert "was not copied" in errors[0]
