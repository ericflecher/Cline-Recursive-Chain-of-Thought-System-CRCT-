# CLI Onboarding Agent

A command-line tool that generates standardized folder structures from templates, designed to streamline and standardize the setup of new domain projects.

## Features

- Generate project structures from template folders
- Exclude guide documents from the generated structure
- Support for custom exclude and include patterns
- Dry run mode to preview changes
- Validation of the generated structure

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd cli-onboarding-agent

# Install the package in development mode
pip install -e .
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
```

## Command-Line Options

- `TARGET_PATH`: The path where the new project structure will be created
- `-t, --template PATH`: Specify the template folder path (default: built-in template)
- `-c, --config PATH`: Specify a configuration file (JSON or YAML)
- `-f, --force`: Force overwrite of existing files without prompting
- `-d, --dry-run`: Show what would be created without making any changes
- `-v, --verbose`: Enable verbose output
- `--exclude PATTERN`: Exclude files matching the pattern (can be specified multiple times)
- `--include PATTERN`: Include files matching the pattern even if they match exclude patterns (can be specified multiple times)
- `-h, --help`: Show help message and exit

## Template Structure

A template folder should have the following structure:

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
├── tests/
│   └── test_main.py               # Main module tests
└── setup.py                       # Package setup file
```

Files with `_guide` in their names are excluded by default. You can customize this behavior using the `--exclude` and `--include` options.

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run tests with coverage
pytest --cov=cli_onboarding_agent
```

## License

MIT
