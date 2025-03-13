"""
Tests for the template_reader module.
"""

import os
import pytest
from pathlib import Path

from cli_onboarding_agent.template_reader import (
    read_template,
    validate_template_structure,
    should_exclude,
    TemplateStructure
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
    
    # Create a guide document that should be excluded
    (template_dir / "README_guide.md").write_text("# Guide Document")
    (template_dir / "docs" / "setup_guide.md").write_text("# Setup Guide")
    
    return template_dir


def test_template_structure_class():
    """Test the TemplateStructure class."""
    structure = TemplateStructure()
    
    # Test adding directories
    structure.add_directory(Path("/test/dir1"))
    structure.add_directory(Path("/test/dir2"))
    assert len(structure.directories) == 2
    
    # Test adding files
    structure.add_file(Path("/test/file1.txt"), {"size": 100})
    structure.add_file(Path("/test/file2.txt"))
    assert len(structure.files) == 2
    assert structure.files[Path("/test/file1.txt")]["size"] == 100
    
    # Test adding excluded files and directories
    structure.add_excluded_file(Path("/test/excluded.txt"))
    structure.add_excluded_directory(Path("/test/excluded_dir"))
    assert len(structure.excluded_files) == 1
    assert len(structure.excluded_directories) == 1
    
    # Test getting relative paths
    base_path = Path("/test")
    rel_dirs = structure.get_relative_directories(base_path)
    assert Path("dir1") in rel_dirs
    assert Path("dir2") in rel_dirs
    
    rel_files = structure.get_relative_files(base_path)
    assert Path("file1.txt") in rel_files
    assert Path("file2.txt") in rel_files
    
    # Test string representation
    str_repr = str(structure)
    assert "directories=2" in str_repr
    assert "files=2" in str_repr
    assert "excluded_files=1" in str_repr
    assert "excluded_directories=1" in str_repr


def test_should_exclude():
    """Test the should_exclude function."""
    # Test with exclude patterns
    assert should_exclude(Path("file.txt"), ["*.txt"], []) is True
    assert should_exclude(Path("file.md"), ["*.txt"], []) is False
    
    # Test with multiple exclude patterns
    assert should_exclude(Path("file.txt"), ["*.md", "*.txt"], []) is True
    
    # Test with include patterns
    assert should_exclude(Path("file.txt"), ["*.txt"], ["file.txt"]) is False
    assert should_exclude(Path("other.txt"), ["*.txt"], ["file.txt"]) is True
    
    # Test with both exclude and include patterns
    assert should_exclude(Path("file_guide.txt"), ["*_guide*"], []) is True
    assert should_exclude(Path("file_guide.txt"), ["*_guide*"], ["*.txt"]) is False


def test_read_template(temp_template_dir):
    """Test the read_template function."""
    # Read the template with default exclude patterns
    structure = read_template(temp_template_dir)
    
    # Check that the correct number of directories were found
    assert len(structure.directories) >= 3  # src, docs, tests
    
    # Check that the correct number of files were found
    assert len(structure.files) >= 4  # README.md, __init__.py, main.py, docs/README.md
    
    # Check that guide documents were excluded
    for file_path in structure.files:
        assert "_guide" not in str(file_path)
    
    # Check that excluded files were recorded
    assert len(structure.excluded_files) >= 2  # README_guide.md, docs/setup_guide.md
    
    # Test with custom exclude patterns
    structure = read_template(temp_template_dir, exclude_patterns=["*.md"])
    
    # Check that .md files were excluded
    for file_path in structure.files:
        assert not str(file_path).endswith(".md")
    
    # Test with include patterns
    structure = read_template(
        temp_template_dir,
        exclude_patterns=["*.md"],
        include_patterns=["README.md"]
    )
    
    # Check that README.md was included despite the exclude pattern
    readme_found = False
    for file_path in structure.files:
        if file_path.name == "README.md":
            readme_found = True
            break
    assert readme_found


def test_validate_template_structure():
    """Test the validate_template_structure function."""
    # Create a valid structure
    valid_structure = TemplateStructure()
    valid_structure.add_directory(Path("/test/dir"))
    valid_structure.add_file(Path("/test/file.txt"))
    
    is_valid, errors = validate_template_structure(valid_structure)
    assert is_valid is True
    assert len(errors) == 0
    
    # Create an invalid structure with no files
    no_files_structure = TemplateStructure()
    no_files_structure.add_directory(Path("/test/dir"))
    
    is_valid, errors = validate_template_structure(no_files_structure)
    assert is_valid is False
    assert len(errors) == 1
    assert "Template contains no files to copy" in errors[0]
    
    # Create an invalid structure with no directories
    no_dirs_structure = TemplateStructure()
    no_dirs_structure.add_file(Path("/test/file.txt"))
    
    is_valid, errors = validate_template_structure(no_dirs_structure)
    assert is_valid is False
    assert len(errors) == 1
    assert "Template contains no directories to create" in errors[0]
    
    # Create an invalid structure with no files and no directories
    empty_structure = TemplateStructure()
    
    is_valid, errors = validate_template_structure(empty_structure)
    assert is_valid is False
    assert len(errors) == 2


def test_read_template_errors():
    """Test error handling in the read_template function."""
    # Test with non-existent template path
    with pytest.raises(FileNotFoundError):
        read_template(Path("/non/existent/path"))
    
    # Test with a file instead of a directory
    temp_file = Path("temp_file.txt")
    try:
        temp_file.write_text("test")
        with pytest.raises(NotADirectoryError):
            read_template(temp_file)
    finally:
        if temp_file.exists():
            temp_file.unlink()
