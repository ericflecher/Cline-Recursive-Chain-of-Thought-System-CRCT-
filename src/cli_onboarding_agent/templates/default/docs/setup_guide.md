# Setup Guide for {{ project_name }}

This is a setup guide document that will be excluded by default when using the CLI Onboarding Agent.

## Development Environment Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests:
   ```bash
   pytest
   ```

## Project Structure

```
{{ project_name }}/
├── README.md                 # Project overview
├── setup.py                  # Package configuration
├── requirements.txt          # Dependencies
├── docs/                     # Documentation
│   └── README.md             # Documentation index
├── src/                      # Source code
│   ├── __init__.py           # Package initialization
│   └── main.py               # Main module
└── tests/                    # Tests
    ├── __init__.py           # Test package initialization
    └── test_main.py          # Tests for main module
```

## Adding New Features

1. Create a new module in the `src` directory
2. Add tests for the new module in the `tests` directory
3. Update the documentation in the `docs` directory
4. Add any new dependencies to `setup.py` and `requirements.txt`
