"""
Validator module for the CLI Onboarding Agent.

This module is responsible for validation checks and testing to ensure
the reliability and correctness of the CLI Onboarding Agent.
"""

import os
import logging
import filecmp
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Set

from cli_onboarding_agent.template_reader import TemplateStructure

logger = logging.getLogger("cli_onboarding_agent")


class ValidationError(Exception):
    """Exception raised for validation errors."""
    pass


def validate_directory_structure(
    target_path: Path,
    template_structure: TemplateStructure,
    template_path: Path
) -> Tuple[bool, List[str]]:
    """
    Validate that the directory structure was created correctly.
    
    Args:
        target_path: The path where the directory structure was created
        template_structure: The template structure that was used
        template_path: The path to the template folder
        
    Returns:
        A tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check that all directories were created
    rel_directories = template_structure.get_relative_directories(template_path)
    for rel_dir in rel_directories:
        dir_path = target_path / rel_dir
        if not dir_path.exists() or not dir_path.is_dir():
            errors.append(f"Directory was not created: {rel_dir}")
    
    return len(errors) == 0, errors


def validate_file_content(
    target_path: Path,
    template_path: Path,
    template_structure: TemplateStructure,
    variables: Dict[str, str] = None
) -> Tuple[bool, List[str]]:
    """
    Validate that the file content was copied correctly.
    
    Args:
        target_path: The path where the files were copied
        template_path: The path to the template folder
        template_structure: The template structure that was used
        variables: Dictionary of variables that were replaced in the file content
        
    Returns:
        A tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check that all files were copied with correct content
    rel_files = template_structure.get_relative_files(template_path)
    for rel_file_path, _ in rel_files.items():
        source_file = template_path / rel_file_path
        target_file = target_path / rel_file_path
        
        # Skip if the source file doesn't exist
        if not source_file.exists() or not source_file.is_file():
            continue
        
        # Check if the target file exists
        if not target_file.exists() or not target_file.is_file():
            errors.append(f"File was not copied: {rel_file_path}")
            continue
        
        # If no variables were replaced, files should be identical
        if not variables:
            if not filecmp.cmp(source_file, target_file, shallow=False):
                errors.append(f"File content differs: {rel_file_path}")
        
        # If variables were replaced, we can't do a direct comparison
        # In a real implementation, we would need a more sophisticated check
    
    return len(errors) == 0, errors


def validate_result(
    target_path: Path,
    template_structure: TemplateStructure,
    template_path: Path,
    variables: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Validate the result of the CLI Onboarding Agent.
    
    Args:
        target_path: The path where the project structure was created
        template_structure: The template structure that was used
        template_path: The path to the template folder
        variables: Dictionary of variables that were replaced in the file content
        
    Returns:
        A dictionary with validation results
        
    Raises:
        ValidationError: If there was an error during validation
    """
    logger.info(f"Validating result at {target_path}")
    
    # Validate directory structure
    dir_valid, dir_errors = validate_directory_structure(
        target_path, template_structure, template_path
    )
    
    # Validate file content
    file_valid, file_errors = validate_file_content(
        target_path, template_path, template_structure, variables
    )
    
    # Combine results
    is_valid = dir_valid and file_valid
    errors = dir_errors + file_errors
    
    # Log results
    if is_valid:
        logger.info("Validation successful")
    else:
        logger.error(f"Validation failed with {len(errors)} errors")
        for error in errors:
            logger.error(f"  - {error}")
    
    return {
        "is_valid": is_valid,
        "directory_structure_valid": dir_valid,
        "file_content_valid": file_valid,
        "errors": errors,
    }


def run_self_test(template_path: Path, target_path: Path) -> Dict[str, Any]:
    """
    Run a self-test of the CLI Onboarding Agent.
    
    Args:
        template_path: The path to a test template folder
        target_path: The path where the test project structure should be created
        
    Returns:
        A dictionary with test results
    """
    from cli_onboarding_agent.template_reader import read_template
    from cli_onboarding_agent.generator import generate_structure
    from cli_onboarding_agent.populator import populate_documents
    
    logger.info(f"Running self-test with template {template_path} and target {target_path}")
    
    results = {
        "template_reader": {"success": False, "errors": []},
        "generator": {"success": False, "errors": []},
        "populator": {"success": False, "errors": []},
        "validator": {"success": False, "errors": []},
        "overall": {"success": False},
    }
    
    try:
        # Test template reader
        template_structure = read_template(template_path)
        results["template_reader"]["success"] = True
        
        # Test generator
        generate_structure(target_path, template_structure, template_path)
        results["generator"]["success"] = True
        
        # Test populator
        populate_documents(target_path, template_path, template_structure)
        results["populator"]["success"] = True
        
        # Test validator
        validation_result = validate_result(target_path, template_structure, template_path)
        results["validator"]["success"] = validation_result["is_valid"]
        results["validator"]["errors"] = validation_result.get("errors", [])
        
        # Overall result
        results["overall"]["success"] = (
            results["template_reader"]["success"] and
            results["generator"]["success"] and
            results["populator"]["success"] and
            results["validator"]["success"]
        )
        
    except Exception as e:
        logger.exception(f"Self-test failed with exception: {str(e)}")
        results["overall"]["exception"] = str(e)
    
    # Log results
    if results["overall"]["success"]:
        logger.info("Self-test passed successfully")
    else:
        logger.error("Self-test failed")
    
    return results
