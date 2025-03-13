"""
CLI entry point for the CLI Onboarding Agent.
"""

import os
import sys
import logging
import click
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("cli_onboarding_agent")

# Import other modules
from cli_onboarding_agent.template_reader import read_template, validate_template_structure
from cli_onboarding_agent.generator import generate_structure, validate_target_path
from cli_onboarding_agent.populator import populate_documents, validate_population
from cli_onboarding_agent.validator import validate_result


@click.command()
@click.argument("target_path", type=click.Path())
@click.option(
    "-t", "--template",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
    help="Path to the template folder. If not provided, a default template will be used."
)
@click.option(
    "-c", "--config",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Path to a configuration file (JSON or YAML)."
)
@click.option(
    "-f", "--force",
    is_flag=True,
    help="Force overwrite of existing files without prompting."
)
@click.option(
    "-d", "--dry-run",
    is_flag=True,
    help="Show what would be created without making any changes."
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Enable verbose output."
)
@click.option(
    "--exclude",
    multiple=True,
    default=["*_guide*"],
    help="Exclude files matching the pattern. Can be specified multiple times."
)
@click.option(
    "--include",
    multiple=True,
    help="Include files matching the pattern even if they match exclude patterns. Can be specified multiple times."
)
def main(target_path, template, config, force, dry_run, verbose, exclude, include):
    """
    Generate a standardized folder structure from a template.

    TARGET_PATH is the path where the new project structure will be created.
    """
    # Set up logging level based on verbose flag
    if verbose:
        logger.setLevel(logging.DEBUG)
    
    # Convert target_path to absolute path
    target_path = Path(target_path).absolute()
    
    # Log the start of the process
    logger.info(f"Starting CLI Onboarding Agent")
    logger.info(f"Target path: {target_path}")
    
    # Validate target path
    if target_path.exists() and not force:
        if not click.confirm(f"Target path {target_path} already exists. Continue?"):
            logger.info("Operation cancelled by user.")
            return
    
    # Log template path
    if template:
        template_path = Path(template).absolute()
        logger.info(f"Template path: {template_path}")
    else:
        logger.info("Using built-in default template")
        # Create a temporary directory with a default template structure
        import tempfile
        import shutil
        
        temp_dir = Path(tempfile.mkdtemp())
        try:
            # Create a basic project structure
            (temp_dir / "src").mkdir()
            (temp_dir / "docs").mkdir()
            (temp_dir / "tests").mkdir()
            
            # Create README.md
            (temp_dir / "README.md").write_text("# Project\n\nProject description\n")
            
            # Create setup.py
            (temp_dir / "setup.py").write_text(
                "from setuptools import setup, find_packages\n\n"
                "setup(\n"
                "    name='project',\n"
                "    version='0.1.0',\n"
                "    packages=find_packages(),\n"
                ")\n"
            )
            
            # Create src/__init__.py
            (temp_dir / "src" / "__init__.py").write_text("")
            
            # Create src/main.py
            (temp_dir / "src" / "main.py").write_text(
                "def main():\n"
                "    print('Hello, world!')\n\n"
                "if __name__ == '__main__':\n"
                "    main()\n"
            )
            
            # Create docs/README.md
            (temp_dir / "docs" / "README.md").write_text("# Documentation\n")
            
            # Create tests/__init__.py
            (temp_dir / "tests" / "__init__.py").write_text("")
            
            # Create tests/test_main.py
            (temp_dir / "tests" / "test_main.py").write_text(
                "import unittest\n\n"
                "class TestMain(unittest.TestCase):\n"
                "    def test_main(self):\n"
                "        self.assertTrue(True)\n"
            )
            
            # Use the temporary directory as the template path
            template_path = temp_dir
            logger.debug(f"Created default template at {template_path}")
            
        except Exception as e:
            logger.error(f"Failed to create default template: {str(e)}")
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise
    
    # Log configuration
    if config:
        config_path = Path(config).absolute()
        logger.info(f"Configuration file: {config_path}")
    
    # Log dry run mode
    if dry_run:
        logger.info("Dry run mode enabled - no changes will be made")
    
    # Log exclude and include patterns
    logger.debug(f"Exclude patterns: {exclude}")
    logger.debug(f"Include patterns: {include}")
    
    # Flag to track if we're using a temporary template directory
    using_temp_template = template is None
    
    try:
        # 1. Read the template structure
        logger.info("Reading template structure...")
        template_structure = read_template(template_path, exclude, include)
        
        # Validate template structure
        is_valid, errors = validate_template_structure(template_structure)
        if not is_valid:
            for error in errors:
                logger.error(f"Template validation error: {error}")
            raise ValueError("Invalid template structure")
        
        # 2. Generate the folder structure
        logger.info("Generating folder structure...")
        if not dry_run:
            generate_structure(target_path, template_structure, template_path, dry_run, force)
        
        # 3. Populate the documents
        logger.info("Populating documents...")
        if not dry_run:
            populate_documents(target_path, template_path, template_structure, dry_run, force)
        
        # 4. Validate the result
        logger.info("Validating result...")
        if not dry_run:
            validation_result = validate_result(target_path, template_structure, template_path)
            if not validation_result["is_valid"]:
                logger.warning("Validation found issues with the generated project structure")
                for error in validation_result["errors"]:
                    logger.warning(f"  - {error}")
        
        # Log completion
        if dry_run:
            logger.info("Dry run completed successfully")
        else:
            logger.info(f"Project structure created successfully at {target_path}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if verbose:
            logger.exception("Detailed error information:")
        
        # Clean up temporary template directory if we created one
        if using_temp_template and template_path and template_path.exists():
            import shutil
            logger.debug(f"Cleaning up temporary template directory: {template_path}")
            shutil.rmtree(template_path, ignore_errors=True)
        
        sys.exit(1)
    
    finally:
        # Clean up temporary template directory if we created one
        if using_temp_template and template_path and template_path.exists():
            import shutil
            logger.debug(f"Cleaning up temporary template directory: {template_path}")
            shutil.rmtree(template_path, ignore_errors=True)


if __name__ == "__main__":
    main()
