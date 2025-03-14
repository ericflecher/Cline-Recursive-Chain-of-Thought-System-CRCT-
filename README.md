# CLI Onboarding Agent

A command-line tool that generates standardized folder structures from templates, designed to streamline and standardize the setup of new domain projects. The tool supports template variable replacement, making it easy to customize generated projects.

## Features

- Generate project structures from template folders
- Replace template variables with custom values
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

### Basic Usage

```bash
# Basic usage with default template
onboard-project new_project

# Specify a custom template
onboard-project --template ~/templates/python_project new_project

# Force overwrite of existing files
onboard-project --force --template ~/templates/python_project existing_project

# Dry run to see what would be created
onboard-project --dry-run --template ~/templates/python_project new_project
```

### Using Template Variables

The CLI tool supports replacing template variables in the generated files. Template variables are specified in the format `{{variable_name}}` in the template files.

```bash
# Specify template variables
onboard-project --template ~/templates/python_project \
  --project-name "My Awesome Project" \
  --package-name "my_awesome_project" \
  --project-description "A super awesome Python project" \
  --author "John Doe" \
  --author-email "john@example.com" \
  new_project
```

### Common Template Variables

- `{{project_name}}`: The name of the project (e.g., "My Awesome Project")
- `{{package_name}}`: The name of the package (e.g., "my_awesome_project")
- `{{project_description}}`: A brief description of the project
- `{{author}}`: The author's name
- `{{author_email}}`: The author's email address

### File Filtering

```bash
# Exclude additional patterns
onboard-project --exclude "*.pyc" --exclude ".DS_Store" new_project

# Include specific guide documents
onboard-project --include "README_guide.md" new_project
```

### Verbose Output

```bash
# Enable verbose output for debugging
onboard-project --verbose --template ~/templates/python_project new_project
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
- `--project-name NAME`: Name of the project (for template variable replacement)
- `--package-name NAME`: Name of the package (for template variable replacement)
- `--project-description DESC`: Description of the project (for template variable replacement)
- `--author NAME`: Author of the project (for template variable replacement)
- `--author-email EMAIL`: Email of the author (for template variable replacement)
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

## Creating Custom Templates

### Template Variables

To create a custom template with variable replacement, use the `{{variable_name}}` syntax in your template files. For example:

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="{{package_name}}",
    version="0.1.0",
    description="{{project_description}}",
    author="{{author}}",
    author_email="{{author_email}}",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add your dependencies here
    ],
    python_requires=">=3.8",
)
```

```markdown
# README.md
# {{project_name}}

{{project_description}}

## Installation

```bash
pip install -e .
```

## Usage

```python
from {{package_name}} import main

main.run()
```
```

### Best Practices for Templates

1. **Use consistent variable naming**: Stick to a consistent naming convention for your template variables.
2. **Document your variables**: Include a README_guide.md file in your template that explains the variables used.
3. **Provide sensible defaults**: Design your templates so they work even if some variables are not provided.
4. **Organize templates by project type**: Create separate templates for different types of projects (e.g., Python libraries, web applications, data science projects).
5. **Include common configuration files**: Include common configuration files like .gitignore, .editorconfig, etc.

## Common Use Cases

### Python Library Template

```bash
onboard-project --template ~/templates/python_library \
  --project-name "My Python Library" \
  --package-name "my_python_library" \
  --project-description "A useful Python library" \
  new_library
```

### Web Application Template

```bash
onboard-project --template ~/templates/flask_app \
  --project-name "My Flask App" \
  --package-name "my_flask_app" \
  --project-description "A web application built with Flask" \
  new_web_app
```

### Data Science Project Template

```bash
onboard-project --template ~/templates/data_science \
  --project-name "My Data Science Project" \
  --package-name "my_data_science_project" \
  --project-description "A data science project with Jupyter notebooks" \
  new_ds_project
```

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

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests
5. Submit a pull request

## License

MIT
