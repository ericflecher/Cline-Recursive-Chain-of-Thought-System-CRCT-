"""
CLI entry point for the CLI Onboarding Agent.

This module provides the command-line interface for the CLI Onboarding Agent,
including AI-powered features for template customization and content generation.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

import click

from cli_onboarding_agent.error_handling import handle_error, CLIError, TemplateError, GenerationError
from cli_onboarding_agent.ui import (
    print_success, print_error, print_warning, print_info, print_header,
    print_step, setup_colored_logging, process_with_progress
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("cli_onboarding_agent")

# Set up colored logging
setup_colored_logging(logger)

# Import other modules
from cli_onboarding_agent.template_reader import read_template, validate_template_structure
from cli_onboarding_agent.generator import generate_structure, validate_target_path
from cli_onboarding_agent.populator import populate_documents, validate_population
from cli_onboarding_agent.validator import validate_result


@click.command()
@click.argument("target_path", type=click.Path())
@click.option(
    "--domains-dir",
    type=click.Path(file_okay=False, dir_okay=True),
    default="domains",
    help="Base directory for all generated projects. Projects will be created under this directory."
)
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
@click.option(
    "--ai-assist",
    is_flag=True,
    help="Enable AI assistance for template customization and content generation."
)
@click.option(
    "--ai-generate-readme",
    is_flag=True,
    help="Use AI to generate or enhance README files."
)
@click.option(
    "--ai-resolve-conflicts",
    is_flag=True,
    help="Use AI to help resolve file conflicts."
)
@click.option(
    "--ai-analyze-template",
    is_flag=True,
    help="Use AI to analyze the template and provide recommendations."
)
@click.option(
    "--ai-generate-docstrings",
    is_flag=True,
    help="Use AI to generate or improve docstrings in code files."
)
@handle_error
def main(target_path, domains_dir, template, config, force, dry_run, verbose, exclude, include,
         project_name, package_name, project_description, author, author_email,
         ai_assist, ai_generate_readme, ai_resolve_conflicts, ai_analyze_template, ai_generate_docstrings):
    """
    Generate a standardized folder structure from a template.

    TARGET_PATH is the path where the new project structure will be created.
    """
    # Set up logging level based on verbose flag
    if verbose:
        logger.setLevel(logging.DEBUG)
        print_info("Verbose mode enabled")
    
    # Ensure projects are created in the domains directory
    domains_path = Path(domains_dir).absolute()
    
    # If target_path is not already within domains_path, place it there
    target_path = Path(target_path)
    if not str(target_path).startswith(str(domains_path)):
        # If target_path is absolute, extract just the name
        if target_path.is_absolute():
            target_name = target_path.name
        else:
            target_name = target_path
        
        # Create the new target path within domains directory
        target_path = domains_path / target_name
    
    # Ensure target_path is absolute
    target_path = target_path.absolute()
    
    # Initialize AI assistant if needed
    ai_assistant = None
    if ai_assist or ai_generate_readme or ai_resolve_conflicts or ai_analyze_template or ai_generate_docstrings:
        try:
            from cli_onboarding_agent.ai_assistant import AIAssistant
            ai_assistant = AIAssistant()
            logger.info("AI assistance enabled")
        except (ImportError, ValueError) as e:
            logger.warning(f"Failed to initialize AI assistant: {str(e)}")
            logger.warning("AI features will be disabled")
    
    # Log the start of the process
    print_header("Starting CLI Onboarding Agent")
    logger.info(f"Domains directory: {domains_path}")
    logger.info(f"Target path: {target_path}")
    
    # Create domains directory if it doesn't exist
    if not domains_path.exists():
        logger.info(f"Creating domains directory: {domains_path}")
        domains_path.mkdir(parents=True, exist_ok=True)
    
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
            error_msg = f"Default template not found at {template_path}"
            logger.error(error_msg)
            raise TemplateError(error_msg, {"template_path": str(template_path)})
    
    # Log configuration
    if config:
        config_path = Path(config).absolute()
        logger.info(f"Configuration file: {config_path}")
    
    # Log dry run mode
    if dry_run:
        print_warning("Dry run mode enabled - no changes will be made")
    
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
        
        # Define the total number of steps
        total_steps = 4
        
        # 1. Read the template structure
        print_step(1, total_steps, "Reading template structure")
        template_structure = read_template(template_path, exclude, include)
        
        # Validate template structure
        is_valid, errors = validate_template_structure(template_structure)
        if not is_valid:
            for error in errors:
                logger.error(f"Template validation error: {error}")
            raise TemplateError("Invalid template structure", {"errors": errors})
        
        # Analyze template with AI if requested
        if ai_assistant and ai_analyze_template:
            logger.info("Analyzing template with AI...")
            analysis = ai_assistant.analyze_template(template_structure)
            
            logger.info(f"AI Template Analysis: {analysis.get('assessment', 'No assessment provided')}")
            
            if analysis.get('suggestions'):
                logger.info("AI Suggestions:")
                for suggestion in analysis.get('suggestions', []):
                    logger.info(f"  - {suggestion}")
            
            if analysis.get('recommendations'):
                logger.info("AI Recommendations:")
                for recommendation in analysis.get('recommendations', []):
                    logger.info(f"  - {recommendation}")
            
            if analysis.get('issues'):
                logger.warning("AI Identified Issues:")
                for issue in analysis.get('issues', []):
                    logger.warning(f"  - {issue}")
        
        # 2. Generate the folder structure
        print_step(2, total_steps, "Generating folder structure")
        if not dry_run:
            generate_structure(target_path, template_structure, template_path, dry_run, force)
        
        # 3. Populate the documents
        print_step(3, total_steps, "Populating documents")
        logger.info(f"Using variables for template replacement: {variables}")
        if not dry_run:
            # Pass AI assistant for conflict resolution if requested
            ai_conflict_resolver = ai_assistant if ai_resolve_conflicts else None
            populate_documents(
                target_path, 
                template_path, 
                template_structure, 
                dry_run, 
                force, 
                variables,
                ai_conflict_resolver
            )
            
            # Generate or enhance README with AI if requested
            if ai_assistant and ai_generate_readme:
                readme_path = target_path / "README.md"
                if readme_path.exists():
                    logger.info("Enhancing README.md with AI...")
                    
                    # Read existing README
                    with open(readme_path, 'r') as f:
                        existing_readme = f.read()
                    
                    # Prepare project info
                    project_info = {
                        "project_name": project_name,
                        "package_name": package_name,
                        "project_description": project_description,
                        "author": author,
                        "author_email": author_email,
                        "structure": template_structure
                    }
                    
                    # Generate enhanced README
                    enhanced_readme = ai_assistant.generate_readme(project_info)
                    
                    # Write enhanced README
                    with open(readme_path, 'w') as f:
                        f.write(enhanced_readme)
                    
                    logger.info("README.md enhanced with AI")
            
            # Generate or improve docstrings with AI if requested
            if ai_assistant and ai_generate_docstrings:
                logger.info("Generating docstrings for Python files...")
                
                # Find all Python files in the target directory
                python_files = list(target_path.glob("**/*.py"))
                
                for py_file in python_files:
                    if py_file.is_file():
                        try:
                            # Read the file
                            with open(py_file, 'r') as f:
                                code = f.read()
                            
                            # Generate improved docstrings
                            improved_code = ai_assistant.generate_docstrings(code, str(py_file))
                            
                            # Write the improved code back to the file
                            with open(py_file, 'w') as f:
                                f.write(improved_code)
                            
                            logger.debug(f"Added docstrings to {py_file.relative_to(target_path)}")
                        except Exception as e:
                            logger.warning(f"Failed to generate docstrings for {py_file}: {str(e)}")
                
                logger.info(f"Generated docstrings for {len(python_files)} Python files")
        
        # 4. Validate the result
        print_step(4, total_steps, "Validating result")
        if not dry_run:
            validation_result = validate_result(target_path, template_structure, template_path)
            if not validation_result["is_valid"]:
                logger.warning("Validation found issues with the generated project structure")
                for error in validation_result["errors"]:
                    logger.warning(f"  - {error}")
        
        # Log completion
        if dry_run:
            print_success("Dry run completed successfully")
        else:
            print_success(f"Project structure created successfully at {target_path}")
        
    except CLIError:
        # These are already handled by the handle_error decorator
        raise
    except Exception as e:
        # Wrap unexpected exceptions in a CLIError
        logger.error(f"Unexpected error: {str(e)}")
        if verbose:
            logger.exception("Detailed error information:")
        raise CLIError(f"Unexpected error: {str(e)}", {"exception_type": type(e).__name__})


if __name__ == "__main__":
    main()
