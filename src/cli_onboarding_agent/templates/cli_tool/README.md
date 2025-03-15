# {{project_name}}

{{description}}

## Features

- Modern Python CLI tool built with Click
- Command-line argument parsing and validation
- Subcommands with help text and documentation
- Logging with different verbosity levels
- Comprehensive test suite

## Installation

### From Source

1. Clone the repository:

```bash
git clone <repository-url>
cd {{project_name}}
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:

```bash
pip install -e .
```

### From PyPI

```bash
pip install {{package_name}}
```

## Usage

After installation, you can use the `{{command_name}}` command:

```bash
# Show help
{{command_name}} --help

# Say hello
{{command_name}} hello
{{command_name}} hello Alice

# Echo a message
{{command_name}} echo "Hello, World!"
{{command_name}} echo -c 3 "Hello, World!"  # Repeat 3 times

# Enable verbose mode
{{command_name}} -v hello
```

## Development

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd {{project_name}}
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code with black
black src tests

# Sort imports with isort
isort src tests

# Check code with flake8
flake8 src tests

# Type checking with mypy
mypy src
```

## Project Structure

```
{{project_name}}/
├── src/                  # Source code
│   └── {{package_name}}/ # Package directory
│       ├── __init__.py   # Package initialization
│       └── cli.py        # CLI implementation
├── tests/                # Test directory
│   └── test_cli.py       # CLI tests
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
├── requirements.txt      # Development dependencies
└── setup.py              # Package configuration
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

{{author}}
