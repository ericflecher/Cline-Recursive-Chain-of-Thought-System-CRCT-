"""
Generator module for the CLI Onboarding Agent.

This module is responsible for generating the folder structure in the target location
based on the template structure.
"""

import os
import logging
import shutil
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from cli_onboarding_agent.template_reader import TemplateStructure

logger = logging.getLogger("cli_onboarding_agent")


class GenerationError(Exception):
    """Exception raised for errors during folder structure generation."""
    pass


def validate_target_path(target_path: Path, force: bool = False) -> Tuple[bool, List[str]]:
    """
    Validate the target path to ensure it's usable.
    
    Args:
        target_path: The target path to validate
        force: Whether to force overwrite of existing files
        
    Returns:
        A tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check if the target path exists
    if target_path.exists():
        if not target_path.is_dir():
            errors.append(f"Target path {target_path} exists but is not a directory")
        elif not os.access(target_path, os.W_OK):
            errors.append(f"Target path {target_path} is not writable")
        elif not force and any(target_path.iterdir()):
            errors.append(f"Target path {target_path} is not empty (use --force to override)")
    else:
        # Check if the parent directory exists and is writable
        parent = target_path.parent
        if not parent.exists():
            errors.append(f"Parent directory {parent} does not exist")
        elif not os.access(parent, os.W_OK):
            errors.append(f"Parent directory {parent} is not writable")
    
    return len(errors) == 0, errors


def create_directory(path: Path, dry_run: bool = False) -> bool:
    """
    Create a directory at the specified path.
    
    Args:
        path: The path where the directory should be created
        dry_run: If True, only log what would be done without making changes
        
    Returns:
        True if the directory was created or already exists, False otherwise
    """
    if dry_run:
        logger.info(f"Would create directory: {path}")
        return True
    
    try:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {path}")
        else:
            logger.debug(f"Directory already exists: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {str(e)}")
        return False


def generate_structure(
    target_path: Path,
    template_structure: TemplateStructure,
    template_path: Path,
    dry_run: bool = False,
    force: bool = False
) -> Dict[str, Any]:
    """
    Generate the folder structure in the target location based on the template structure.
    
    Args:
        target_path: The path where the folder structure should be created
        template_structure: The template structure to use
        template_path: The path to the template folder
        dry_run: If True, only log what would be done without making changes
        force: If True, overwrite existing files without prompting
        
    Returns:
        A dictionary with statistics about the generation process
        
    Raises:
        GenerationError: If there was an error during generation
    """
    logger.info(f"Generating folder structure at {target_path}")
    
    # Validate target path
    is_valid, errors = validate_target_path(target_path, force)
    if not is_valid:
        raise GenerationError(f"Invalid target path: {'; '.join(errors)}")
    
    # Create the target directory if it doesn't exist
    if not dry_run and not target_path.exists():
        try:
            target_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created target directory: {target_path}")
        except Exception as e:
            raise GenerationError(f"Failed to create target directory: {str(e)}")
    
    # Statistics
    stats = {
        "directories_created": 0,
        "directories_skipped": 0,
        "directories_failed": 0,
    }
    
    # Create directories
    rel_directories = template_structure.get_relative_directories(template_path)
    for rel_dir in sorted(rel_directories):
        dir_path = target_path / rel_dir
        
        if create_directory(dir_path, dry_run):
            stats["directories_created"] += 1
        else:
            stats["directories_failed"] += 1
    
    logger.info(f"Folder structure generation completed: {stats}")
    return stats


def cleanup_failed_generation(target_path: Path, created_paths: List[Path]) -> None:
    """
    Clean up after a failed generation by removing created directories.
    
    Args:
        target_path: The target path where generation was attempted
        created_paths: List of paths that were created during generation
    """
    logger.info(f"Cleaning up after failed generation at {target_path}")
    
    # Sort paths in reverse order to remove deepest paths first
    for path in sorted(created_paths, reverse=True):
        try:
            if path.is_dir() and path.exists():
                # Check if the directory is empty or contains only empty directories
                is_empty = True
                for item in path.iterdir():
                    if item.is_file():
                        is_empty = False
                        break
                
                if is_empty:
                    # Try to remove any empty subdirectories first
                    for subdir in path.iterdir():
                        if subdir.is_dir() and not any(subdir.iterdir()):
                            subdir.rmdir()
                            logger.debug(f"Removed directory: {subdir}")
                    
                    # Check again if the directory is now empty
                    if not any(path.iterdir()):
                        path.rmdir()
                        logger.debug(f"Removed directory: {path}")
        except Exception as e:
            logger.error(f"Failed to remove directory {path}: {str(e)}")
