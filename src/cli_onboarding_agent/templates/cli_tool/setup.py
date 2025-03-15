"""
Setup script for {{project_name}}.

This script defines the package metadata, dependencies, and entry points
for the CLI tool.
"""

from setuptools import setup, find_packages

setup(
    name="{{package_name}}",
    version="{{version}}",
    description="{{description}}",
    author="{{author}}",
    author_email="{{author_email}}",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "{{command_name}}={{package_name}}.cli:cli",
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
    ],
    python_requires=">=3.8",
)
