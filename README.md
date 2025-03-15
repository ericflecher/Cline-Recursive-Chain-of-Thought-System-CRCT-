# CLI Onboarding Agent

A powerful command-line tool for generating standardized project structures from templates with AI-powered enhancements.

## Features

- **Template-Based Project Generation**: Create consistent project structures from templates
- **AI-Powered Capabilities**: Template analysis, README generation, conflict resolution, docstring generation
- **User-Friendly Interface**: Color-coded output, progress bars, step-by-step visualization
- **Flexible Configuration**: Custom variables, include/exclude patterns, dry run mode
- **Robust Error Handling**: Comprehensive exception handling, detailed error messages

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cli-onboarding-agent.git
cd cli-onboarding-agent

# Install the package
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Usage

### Basic Usage

```bash
# Create a new project using the default template
onboard-project my-new-project

# Create a new project using a custom template
onboard-project my-new-project --template path/to/template

# Create a new project with specific variables
onboard-project my-new-project --project-name "My Project" --author "Your Name"
```

### AI-Powered Features

```bash
# Enable AI assistance
onboard-project my-new-project --ai-assist

# Generate an enhanced README with AI
onboard-project my-new-project --ai-generate-readme

# Resolve conflicts with AI
onboard-project my-new-project --ai-resolve-conflicts

# Analyze the template with AI
onboard-project my-new-project --ai-analyze-template

# Generate docstrings with AI
onboard-project my-new-project --ai-generate-docstrings
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/

# Run specific tests
pytest src/tests/test_cli.py
```

### Code Quality

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint code with flake8
flake8 .

# Type check with mypy
mypy src/

# Run all pre-commit hooks
pre-commit run --all-files
```

## License

MIT
