"""
Setup script for the CLI Onboarding Agent.

This script defines the package metadata, dependencies, and entry points
for the CLI Onboarding Agent.
"""

import os
from setuptools import setup, find_packages

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, '..', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="cli_onboarding_agent",
    version="0.1.0",
    description="A CLI tool to generate standardized folder structures from templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cline Team",
    author_email="team@example.com",
    url="https://github.com/cline-team/cli-onboarding-agent",
    license="MIT",
    keywords="cli, template, project structure, code generation, ai, openai",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "openai>=1.0.0",
        "tqdm>=4.65.0",
        "colorama>=0.4.6",  # For Windows color support
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "hypothesis>=6.70.0",
            "black>=23.3.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "flake8-docstrings>=1.7.0",
            "mypy>=1.3.0",
            "pre-commit>=3.3.2",
            "types-requests>=2.30.0.0",
            "build",
            "twine",
        ],
    },
    entry_points={
        "console_scripts": [
            "onboard-project=cli_onboarding_agent.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "cli_onboarding_agent": ["templates/**/*"],
    },
)
