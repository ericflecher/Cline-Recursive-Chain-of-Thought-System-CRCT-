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
@click.option(
    "--project-name",
    help="Name of the project. Used to replace {{project_name}} in template files."
)
@click.option(
    "--package-name",
    help="Name of the package. Used to replace {{package_name}} in template files."
)
@click.option(
    "--project-description",
    help="Description of the project. Used to replace {{project_description}} in template files."
)
@click.option(
    "--author",
    help="Author of the project. Used to replace {{author}} in template files."
)
@click.option(
    "--author-email",
    help="Email of the author. Used to replace {{author_email}} in template files."
)
def main(target_path, template, config, force, dry_run, verbose, exclude, include,
         project_name, package_name, project_description, author, author_email):
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
        # Use the default template in the package
        template_path = Path(__file__).parent / "templates" / "default"
        logger.debug(f"Using default template at {template_path}")
        
        if not template_path.exists() or not template_path.is_dir():
            logger.error(f"Default template not found at {template_path}")
            raise FileNotFoundError(f"Default template not found at {template_path}")
    
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
    
    # We're no longer using a temporary template directory
    
    try:
        # Prepare variables for template replacement
        variables = {}
        
        # Extract project name from target path if not provided
        if not project_name:
            project_name = Path(target_path).name
            logger.info(f"Using target directory name as project name: {project_name}")
        variables["project_name"] = project_name
        
        # Use project_name as package_name if not provided, but convert to snake_case
        if not package_name:
            package_name = project_name.lower().replace("-", "_").replace(" ", "_")
            logger.info(f"Using derived package name: {package_name}")
        variables["package_name"] = package_name
        
        # Set default values for other variables if not provided
        if not project_description:
            project_description = f"A Python project named {project_name}"
            logger.info(f"Using default project description: {project_description}")
        variables["project_description"] = project_description
        
        if not author:
            import getpass
            author = getpass.getuser()
            logger.info(f"Using current user as author: {author}")
        variables["author"] = author
        
        if not author_email:
            author_email = f"{author.lower().replace(' ', '.')}@example.com"
            logger.info(f"Using default author email: {author_email}")
        variables["author_email"] = author_email
        
        logger.debug(f"Template variables: {variables}")
        
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
        logger.info(f"Using variables for template replacement: {variables}")
        if not dry_run:
            populate_documents(target_path, template_path, template_structure, dry_run, force, variables)
        
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
        sys.exit(1)


if __name__ == "__main__":
    main()
