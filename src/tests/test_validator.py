"""
Tests for the validator module.
"""

import os
import pytest
from pathlib import Path

from cli_onboarding_agent.template_reader import TemplateStructure, read_template
from cli_onboarding_agent.generator import generate_structure
from cli_onboarding_agent.populator import populate_documents
from cli_onboarding_agent.validator import (
    validate_result,
    validate_directory_structure,
    validate_file_content,
    ValidationError,
    run_self_test
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
def populated_target_dir(temp_target_dir, temp_template_dir, template_structure):
    """Fixture for creating a fully populated target directory."""
    # Generate the folder structure
    generate_structure(
        temp_target_dir,
        template_structure,
        temp_template_dir,
        dry_run=False,
        force=False
    )
    
    # Populate the documents
    populate_documents(
        temp_target_dir,
        temp_template_dir,
        template_structure,
        dry_run=False,
        force=False
    )
    
    return temp_target_dir


def test_validate_directory_structure(populated_target_dir, temp_template_dir, template_structure):
    """Test the validate_directory_structure function."""
    # Validate a correctly populated directory structure
    is_valid, errors = validate_directory_structure(
        populated_target_dir,
        template_structure,
        temp_template_dir
    )
    
    assert is_valid is True
    assert len(errors) == 0
    
    # Remove a directory and its contents
    import shutil
    shutil.rmtree(populated_target_dir / "src")
    
    is_valid, errors = validate_directory_structure(
        populated_target_dir,
        template_structure,
        temp_template_dir
    )
    
    assert is_valid is False
    assert len(errors) == 1
    assert "was not created" in errors[0]


def test_validate_file_content(populated_target_dir, temp_template_dir, template_structure):
    """Test the validate_file_content function."""
    # Validate a correctly populated file content
    is_valid, errors = validate_file_content(
        populated_target_dir,
        temp_template_dir,
        template_structure
    )
    
    assert is_valid is True
    assert len(errors) == 0
    
    # Modify a file and validate again
    (populated_target_dir / "README.md").write_text("Modified content")
    
    is_valid, errors = validate_file_content(
        populated_target_dir,
        temp_template_dir,
        template_structure
    )
    
    assert is_valid is False
    assert len(errors) == 1
    assert "content differs" in errors[0]
    
    # Remove a file and validate again
    (populated_target_dir / "src" / "main.py").unlink()
    
    is_valid, errors = validate_file_content(
        populated_target_dir,
        temp_template_dir,
        template_structure
    )
    
    assert is_valid is False
    assert len(errors) >= 2  # At least 2 errors (modified README.md and missing main.py)
    assert any("was not copied" in error for error in errors)


def test_validate_result(populated_target_dir, temp_template_dir, template_structure):
    """Test the validate_result function."""
    # Validate a correctly populated project structure
    result = validate_result(
        populated_target_dir,
        template_structure,
        temp_template_dir
    )
    
    assert result["is_valid"] is True
    assert result["directory_structure_valid"] is True
    assert result["file_content_valid"] is True
    assert len(result["errors"]) == 0
    
    # Modify a file and validate again
    (populated_target_dir / "README.md").write_text("Modified content")
    
    result = validate_result(
        populated_target_dir,
        template_structure,
        temp_template_dir
    )
    
    assert result["is_valid"] is False
    assert result["directory_structure_valid"] is True
    assert result["file_content_valid"] is False
    assert len(result["errors"]) == 1
    assert "content differs" in result["errors"][0]
    
    # Remove a directory and validate again
    (populated_target_dir / "tests").rmdir()
    
    result = validate_result(
        populated_target_dir,
        template_structure,
        temp_template_dir
    )
    
    assert result["is_valid"] is False
    assert result["directory_structure_valid"] is False
    assert result["file_content_valid"] is False
    assert len(result["errors"]) >= 2  # At least 2 errors (modified README.md and missing tests directory)


def test_run_self_test(temp_template_dir, tmp_path):
    """Test the run_self_test function."""
    # Create a target directory for the self-test
    test_target_dir = tmp_path / "self_test_target"
    
    # Run the self-test
    results = run_self_test(temp_template_dir, test_target_dir)
    
    # Check the results
    assert results["template_reader"]["success"] is True
    assert results["generator"]["success"] is True
    assert results["populator"]["success"] is True
    assert results["validator"]["success"] is True
    assert results["overall"]["success"] is True
    
    # Check that the target directory was created and populated
    assert test_target_dir.exists()
    assert (test_target_dir / "README.md").exists()
    assert (test_target_dir / "src" / "main.py").exists()
    
    # Check that guide documents were excluded
    assert not (test_target_dir / "README_guide.md").exists()
