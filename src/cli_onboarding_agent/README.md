# CLI Onboarding Agent

A command-line interface (CLI) tool that generates a standardized folder structure for new domain projects, pre-populated with template documents.

## Installation

```bash
# Install from the current directory
pip install -e .

# Or install from PyPI (once published)
pip install cli_onboarding_agent
```

## Usage

```bash
# Basic usage with default template
onboard-project new_project

# Specify a custom template
onboard-project --template ~/templates/python_project new_project

# Force overwrite of existing files
onboard-project --force --template ~/templates/python_project existing_project

# Dry run to see what would be created
onboard-project --dry-run --template ~/templates/python_project new_project

# Exclude additional patterns
onboard-project --exclude "*.pyc" --exclude ".DS_Store" new_project

# Include specific guide documents
onboard-project --include "README_guide.md" new_project

# Specify project variables
onboard-project --project-name "My Project" --author "John Doe" new_project
```

## Features

- Generate standardized folder structures from templates
- Exclude guide documents (identified by "_guide" in their names)
- Replace template variables in files
- Validate the generated structure
- Dry run mode to preview changes
- Force overwrite option for existing files
- Verbose logging for detailed progress information

## Template Variables

The following template variables are available:

- `{{ project_name }}`: The name of the project
- `{{ package_name }}`: The name of the package (usually a snake_case version of the project name)
- `{{ project_description }}`: A description of the project
- `{{ author }}`: The author of the project
- `{{ author_email }}`: The email of the author

## Creating Custom Templates

You can create custom templates by following the structure of the default template:

```
template_folder/
├── README.md                      # Project overview
├── README_guide.md                # Guide document (will be excluded)
├── docs/
│   ├── requirements.md            # Requirements documentation
│   └── setup_guide.md             # Guide document (will be excluded)
├── src/
│   ├── __init__.py                # Package initialization
│   └── main.py                    # Main module
└── tests/
    ├── __init__.py                # Test package initialization
    └── test_main.py               # Main module tests
```

Files with "_guide" in their names will be excluded by default when generating a new project structure.

## Development

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Run tests: `pytest`
