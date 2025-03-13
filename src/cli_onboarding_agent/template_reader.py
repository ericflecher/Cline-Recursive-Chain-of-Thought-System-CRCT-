"""
Template reader module for the CLI Onboarding Agent.

This module is responsible for reading the template folder structure and
identifying which files should be copied to the target location.
"""

import os
import logging
import fnmatch
from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Tuple

logger = logging.getLogger("cli_onboarding_agent")


class TemplateStructure:
    """
    Represents the structure of a template folder.
    """
    
    def __init__(self):
        self.directories: Set[Path] = set()
        self.files: Dict[Path, Dict[str, Any]] = {}
        self.excluded_files: Set[Path] = set()
        self.excluded_directories: Set[Path] = set()
    
    def add_directory(self, path: Path) -> None:
        """Add a directory to the structure."""
        self.directories.add(path)
    
    def add_file(self, path: Path, metadata: Dict[str, Any] = None) -> None:
        """Add a file to the structure with optional metadata."""
        self.files[path] = metadata or {}
    
    def add_excluded_file(self, path: Path) -> None:
        """Add a file to the excluded files set."""
        self.excluded_files.add(path)
    
    def add_excluded_directory(self, path: Path) -> None:
        """Add a directory to the excluded directories set."""
        self.excluded_directories.add(path)
    
    def get_relative_directories(self, base_path: Path) -> Set[Path]:
        """Get all directories as paths relative to the base path."""
        return {path.relative_to(base_path) for path in self.directories}
    
    def get_relative_files(self, base_path: Path) -> Dict[Path, Dict[str, Any]]:
        """Get all files as paths relative to the base path with their metadata."""
        return {path.relative_to(base_path): metadata 
                for path, metadata in self.files.items()}
    
    def __str__(self) -> str:
        """String representation of the template structure."""
        return (f"TemplateStructure(directories={len(self.directories)}, "
                f"files={len(self.files)}, "
                f"excluded_files={len(self.excluded_files)}, "
                f"excluded_directories={len(self.excluded_directories)})")


def should_exclude(path: Path, exclude_patterns: List[str], include_patterns: List[str]) -> bool:
    """
    Determine if a path should be excluded based on the exclude and include patterns.
    
    Args:
        path: The path to check
        exclude_patterns: List of glob patterns to exclude
        include_patterns: List of glob patterns to include even if they match exclude patterns
        
    Returns:
        True if the path should be excluded, False otherwise
    """
    # Check if the path matches any include pattern
    path_str = str(path)
    for pattern in include_patterns:
        if fnmatch.fnmatch(path_str, pattern):
            return False
    
    # Check if the path matches any exclude pattern
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path_str, pattern):
            return True
    
    return False


def read_template(
    template_path: Path,
    exclude_patterns: List[str] = None,
    include_patterns: List[str] = None
) -> TemplateStructure:
    """
    Read the template folder structure and identify which files should be copied.
    
    Args:
        template_path: Path to the template folder
        exclude_patterns: List of glob patterns to exclude
        include_patterns: List of glob patterns to include even if they match exclude patterns
        
    Returns:
        A TemplateStructure object representing the template folder structure
        
    Raises:
        FileNotFoundError: If the template path does not exist
        NotADirectoryError: If the template path is not a directory
        PermissionError: If the template path is not readable
    """
    exclude_patterns = exclude_patterns or ["*_guide*"]
    include_patterns = include_patterns or []
    
    # Validate template path
    if not template_path.exists():
        raise FileNotFoundError(f"Template path {template_path} does not exist")
    if not template_path.is_dir():
        raise NotADirectoryError(f"Template path {template_path} is not a directory")
    if not os.access(template_path, os.R_OK):
        raise PermissionError(f"Template path {template_path} is not readable")
    
    logger.info(f"Reading template structure from {template_path}")
    logger.debug(f"Exclude patterns: {exclude_patterns}")
    logger.debug(f"Include patterns: {include_patterns}")
    
    structure = TemplateStructure()
    
    # Walk the template directory
    for root, dirs, files in os.walk(template_path):
        root_path = Path(root)
        
        # Process directories
        for dir_name in dirs:
            dir_path = root_path / dir_name
            rel_dir_path = dir_path.relative_to(template_path)
            
            if should_exclude(rel_dir_path, exclude_patterns, include_patterns):
                structure.add_excluded_directory(dir_path)
                logger.debug(f"Excluding directory: {rel_dir_path}")
            else:
                structure.add_directory(dir_path)
                logger.debug(f"Including directory: {rel_dir_path}")
        
        # Process files
        for file_name in files:
            file_path = root_path / file_name
            rel_file_path = file_path.relative_to(template_path)
            
            if should_exclude(rel_file_path, exclude_patterns, include_patterns):
                structure.add_excluded_file(file_path)
                logger.debug(f"Excluding file: {rel_file_path}")
            else:
                # Add basic metadata
                metadata = {
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime,
                }
                structure.add_file(file_path, metadata)
                logger.debug(f"Including file: {rel_file_path}")
    
    logger.info(f"Template structure read: {structure}")
    return structure


def validate_template_structure(structure: TemplateStructure) -> Tuple[bool, List[str]]:
    """
    Validate the template structure to ensure it's usable.
    
    Args:
        structure: The template structure to validate
        
    Returns:
        A tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check if there are any files to copy
    if not structure.files:
        errors.append("Template contains no files to copy")
    
    # Check if there are any directories to create
    if not structure.directories:
        errors.append("Template contains no directories to create")
    
    return len(errors) == 0, errors
