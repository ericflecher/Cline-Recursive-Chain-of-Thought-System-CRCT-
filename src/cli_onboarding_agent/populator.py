"""
Populator module for the CLI Onboarding Agent.

This module is responsible for copying template documents to the target structure,
ensuring all non-guide documents are properly transferred. It also provides
conflict resolution capabilities, including AI-powered conflict resolution.
"""

import os
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Set, Union, Callable

from cli_onboarding_agent.ui import process_with_progress

from cli_onboarding_agent.template_reader import TemplateStructure

logger = logging.getLogger("cli_onboarding_agent")


class PopulationError(Exception):
    """Exception raised for errors during document population."""
    pass


def should_overwrite_file(target_file: Path, force: bool = False) -> bool:
    """
    Determine if a file should be overwritten.
    
    Args:
        target_file: The target file path
        force: Whether to force overwrite without prompting
        
    Returns:
        True if the file should be overwritten, False otherwise
    """
    if not target_file.exists():
        return True
    
    if force:
        return True
    
    # In a real implementation, this would prompt the user
    # For now, we'll just return False to be safe
    return False


def copy_file(
    source_file: Path,
    target_file: Path,
    dry_run: bool = False,
    force: bool = False,
    ai_assistant: Optional[Any] = None
) -> bool:
    """
    Copy a file from source to target.
    
    Args:
        source_file: The source file path
        target_file: The target file path
        dry_run: If True, only log what would be done without making changes
        force: If True, overwrite existing files without prompting
        
    Returns:
        True if the file was copied successfully, False otherwise
    """
    if dry_run:
        logger.info(f"Would copy file: {source_file} -> {target_file}")
        return True
    
    try:
        # Check if the target file exists
        if target_file.exists():
            # If AI assistant is available and the file is a text file, try to resolve conflicts
            if ai_assistant and is_text_file(target_file):
                try:
                    # Read the source and target files
                    with open(source_file, 'r', encoding='utf-8') as f:
                        source_content = f.read()
                    
                    with open(target_file, 'r', encoding='utf-8') as f:
                        target_content = f.read()
                    
                    # Use AI to resolve conflicts
                    logger.info(f"Using AI to resolve conflicts in {target_file}")
                    merged_content, explanation = ai_assistant.resolve_conflict(
                        source_content, target_content, str(target_file)
                    )
                    
                    # Write the merged content to the target file
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(merged_content)
                    
                    logger.info(f"AI conflict resolution for {target_file}: {explanation[:100]}...")
                    return True
                except Exception as e:
                    logger.error(f"AI conflict resolution failed for {target_file}: {str(e)}")
                    # Fall back to normal behavior
            
            # If no AI resolution or it failed, check if we should overwrite
            if not should_overwrite_file(target_file, force):
                logger.debug(f"Skipping existing file: {target_file}")
                return False
        
        # Ensure the target directory exists
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        shutil.copy2(source_file, target_file)
        logger.debug(f"Copied file: {source_file} -> {target_file}")
        return True
    except Exception as e:
        logger.error(f"Failed to copy file {source_file} to {target_file}: {str(e)}")
        return False


def is_text_file(file_path: Path) -> bool:
    """
    Check if a file is a text file.
    
    Args:
        file_path: The file path to check
        
    Returns:
        True if the file is a text file, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)  # Try to read some content
        return True
    except UnicodeDecodeError:
        return False


def process_file_content(
    source_file: Path,
    target_file: Path,
    variables: Dict[str, str] = None,
    ai_assistant: Optional[Any] = None
) -> bool:
    """
    Process file content during copying, e.g., replacing template variables.
    
    Args:
        source_file: The source file path
        target_file: The target file path
        variables: Dictionary of variables to replace in the file content
        
    Returns:
        True if the file was processed successfully, False otherwise
    """
    if not variables:
        logger.warning(f"No variables provided for template replacement in {source_file}")
        return True  # No processing needed
    
    try:
        # Read the source file
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info(f"Processing file content for {target_file}")
        logger.info(f"Variables: {variables}")
        logger.info(f"Original content (first 100 chars): {content[:100]}")
        
        # Check if the file contains any template variables
        original_content = content
        
        # Replace variables
        for key, value in variables.items():
            # Try both formats: with and without spaces
            placeholder_with_spaces = f"{{{{ {key} }}}}"
            placeholder_without_spaces = f"{{{{{key}}}}}"
            
            logger.info(f"Looking for placeholders: '{placeholder_with_spaces}' or '{placeholder_without_spaces}' in {target_file}")
            
            if placeholder_with_spaces in content:
                logger.info(f"Found placeholder: '{placeholder_with_spaces}' in {target_file}")
                logger.info(f"Replacing '{placeholder_with_spaces}' with '{value}' in {target_file}")
                content = content.replace(placeholder_with_spaces, value)
            
            if placeholder_without_spaces in content:
                logger.info(f"Found placeholder: '{placeholder_without_spaces}' in {target_file}")
                logger.info(f"Replacing '{placeholder_without_spaces}' with '{value}' in {target_file}")
                content = content.replace(placeholder_without_spaces, value)
            
            if placeholder_with_spaces not in content and placeholder_without_spaces not in content:
                logger.warning(f"Neither placeholder '{placeholder_with_spaces}' nor '{placeholder_without_spaces}' found in {target_file}")
        
        # Check if any replacements were made
        if content == original_content:
            logger.warning(f"No template variables were replaced in {target_file}")
            logger.info(f"Content after replacement (first 100 chars): {content[:100]}")
        
        # Write to the target file
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Processed file content: {target_file}")
        return True
    except UnicodeDecodeError:
        # Not a text file, just copy it
        logger.debug(f"Skipping content processing for binary file: {source_file}")
        return shutil.copy2(source_file, target_file) is not None
    except Exception as e:
        logger.error(f"Failed to process file content {source_file}: {str(e)}")
        return False


def populate_documents(
    target_path: Path,
    template_path: Path,
    template_structure: TemplateStructure,
    dry_run: bool = False,
    force: bool = False,
    variables: Dict[str, str] = None,
    ai_assistant: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Copy template documents to the target structure.
    
    Args:
        target_path: The path where the documents should be copied
        template_path: The path to the template folder
        template_structure: The template structure to use
        dry_run: If True, only log what would be done without making changes
        force: If True, overwrite existing files without prompting
        variables: Dictionary of variables to replace in the file content
        
    Returns:
        A dictionary with statistics about the population process
        
    Raises:
        PopulationError: If there was an error during population
    """
    logger.info(f"Populating documents at {target_path}")
    
    # Statistics
    stats = {
        "files_copied": 0,
        "files_skipped": 0,
        "files_failed": 0,
    }
    
    # Get all files to copy
    rel_files = template_structure.get_relative_files(template_path)
    file_items = []
    
    # Prepare file items for processing
    for rel_file_path, metadata in rel_files.items():
        source_file = template_path / rel_file_path
        target_file = target_path / rel_file_path
        
        # Skip if the source file doesn't exist
        if not source_file.exists() or not source_file.is_file():
            logger.warning(f"Source file does not exist or is not a file: {source_file}")
            stats["files_skipped"] += 1
            continue
        
        file_items.append((source_file, target_file))
    
    # Define the file processing function
    def process_file(item: Tuple[Path, Path]) -> Dict[str, Any]:
        source_file, target_file = item
        result = {
            "copied": False,
            "skipped": False,
            "failed": False,
            "file": str(target_file.relative_to(target_path))
        }
        
        # Copy the file
        if copy_file(source_file, target_file, dry_run, force, ai_assistant):
            # Process file content if needed
            if not dry_run and variables:
                if process_file_content(source_file, target_file, variables, ai_assistant):
                    result["copied"] = True
                else:
                    result["failed"] = True
            else:
                result["copied"] = True
        else:
            result["skipped"] = True
        
        return result
    
    # Process files with progress bar
    if not dry_run and file_items:
        results = process_with_progress(
            file_items,
            process_file,
            desc="Copying files",
            unit="file"
        )
        
        # Update statistics
        for result in results:
            if result["copied"]:
                stats["files_copied"] += 1
            elif result["skipped"]:
                stats["files_skipped"] += 1
            elif result["failed"]:
                stats["files_failed"] += 1
    elif dry_run:
        # In dry run mode, just log what would be done
        for source_file, target_file in file_items:
            logger.info(f"Would copy file: {source_file} -> {target_file}")
            stats["files_copied"] += 1
    
    logger.info(f"Document population completed: {stats}")
    return stats


def validate_population(
    target_path: Path,
    template_structure: TemplateStructure,
    template_path: Path
) -> Tuple[bool, List[str]]:
    """
    Validate that the document population was successful.
    
    Args:
        target_path: The path where the documents were copied
        template_structure: The template structure that was used
        template_path: The path to the template folder
        
    Returns:
        A tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check that all files were copied
    rel_files = template_structure.get_relative_files(template_path)
    for rel_file_path, _ in rel_files.items():
        target_file = target_path / rel_file_path
        if not target_file.exists() or not target_file.is_file():
            errors.append(f"File was not copied: {rel_file_path}")
    
    return len(errors) == 0, errors
