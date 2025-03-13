"""
Tests for the generator module.
"""

import os
import pytest
from pathlib import Path

from cli_onboarding_agent.template_reader import TemplateStructure, read_template
from cli_onboarding_agent.generator import (
    generate_structure,
    validate_target_path,
    create_directory,
    GenerationError,
    cleanup_failed_generation
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
    
    return template_dir


@pytest.fixture
def temp_target_dir(tmp_path):
    """Fixture for creating a temporary target directory."""
    target_dir = tmp_path / "target"
    return target_dir


@pytest.fixture
def template_structure(temp_template_dir):
    """Fixture for creating a template structure."""
    return read_template(temp_template_dir)


def test_validate_target_path(temp_target_dir):
    """Test the validate_target_path function."""
    # Test with non-existent target path
    is_valid, errors = validate_target_path(temp_target_dir)
    assert is_valid is True
    assert len(errors) == 0
    
    # Create the target directory
    temp_target_dir.mkdir()
    
    # Test with existing empty target path
    is_valid, errors = validate_target_path(temp_target_dir)
    assert is_valid is True
    assert len(errors) == 0
    
    # Create a file in the target directory
    (temp_target_dir / "test.txt").write_text("test")
    
    # Test with existing non-empty target path without force
    is_valid, errors = validate_target_path(temp_target_dir, force=False)
    assert is_valid is False
    assert len(errors) == 1
    assert "not empty" in errors[0]
    
    # Test with existing non-empty target path with force
    is_valid, errors = validate_target_path(temp_target_dir, force=True)
    assert is_valid is True
    assert len(errors) == 0
    
    # Test with a file instead of a directory
    file_path = temp_target_dir.parent / "file.txt"
    file_path.write_text("test")
    
    is_valid, errors = validate_target_path(file_path)
    assert is_valid is False
    assert len(errors) == 1
    assert "not a directory" in errors[0]


def test_create_directory(temp_target_dir):
    """Test the create_directory function."""
    # Test creating a directory
    result = create_directory(temp_target_dir)
    assert result is True
    assert temp_target_dir.exists()
    assert temp_target_dir.is_dir()
    
    # Test creating a nested directory
    nested_dir = temp_target_dir / "nested" / "dir"
    result = create_directory(nested_dir)
    assert result is True
    assert nested_dir.exists()
    assert nested_dir.is_dir()
    
    # Test with dry run
    dry_run_dir = temp_target_dir / "dry_run"
    result = create_directory(dry_run_dir, dry_run=True)
    assert result is True
    assert not dry_run_dir.exists()


def test_generate_structure(temp_template_dir, temp_target_dir, template_structure):
    """Test the generate_structure function."""
    # Generate the structure
    stats = generate_structure(
        temp_target_dir,
        template_structure,
        temp_template_dir,
        dry_run=False,
        force=False
    )
    
    # Check that the target directory was created
    assert temp_target_dir.exists()
    assert temp_target_dir.is_dir()
    
    # Check that the expected directories were created
    assert (temp_target_dir / "src").exists()
    assert (temp_target_dir / "docs").exists()
    assert (temp_target_dir / "tests").exists()
    
    # Check the statistics
    assert stats["directories_created"] >= 3  # src, docs, tests
    assert stats["directories_failed"] == 0
    
    # Test with dry run
    dry_run_dir = temp_target_dir.parent / "dry_run"
    stats = generate_structure(
        dry_run_dir,
        template_structure,
        temp_template_dir,
        dry_run=True,
        force=False
    )
    
    # Check that the target directory was not created
    assert not dry_run_dir.exists()


def test_generate_structure_errors(temp_template_dir, template_structure):
    """Test error handling in the generate_structure function."""
    # Test with a file instead of a directory
    file_path = Path("test_file.txt")
    try:
        file_path.write_text("test")
        with pytest.raises(GenerationError):
            generate_structure(
                file_path,
                template_structure,
                temp_template_dir,
                dry_run=False,
                force=False
            )
    finally:
        if file_path.exists():
            file_path.unlink()


def test_cleanup_failed_generation(tmp_path):
    """Test the cleanup_failed_generation function."""
    # Create a directory structure
    target_dir = tmp_path / "target"
    target_dir.mkdir()
    
    nested_dir1 = target_dir / "nested1"
    nested_dir1.mkdir()
    
    nested_dir2 = target_dir / "nested2"
    nested_dir2.mkdir()
    
    deep_nested_dir = nested_dir2 / "deep"
    deep_nested_dir.mkdir()
    
    # Create a file in one of the directories
    (nested_dir1 / "file.txt").write_text("test")
    
    # Create a list of created paths
    created_paths = [
        target_dir,
        nested_dir1,
        nested_dir2,
        deep_nested_dir
    ]

    # Clean up
    cleanup_failed_generation(target_dir, created_paths)

    # Check that empty directories were removed
    assert not deep_nested_dir.exists()
    # Our implementation now removes empty parent directories too
    assert not nested_dir2.exists()  # Parent of deep_nested_dir is now removed
    assert nested_dir1.exists()  # Contains a file
    assert target_dir.exists()   # Root directory
