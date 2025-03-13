"""
Setup script for the CLI Onboarding Agent.
"""

from setuptools import setup, find_packages

setup(
    name="cli_onboarding_agent",
    version="0.1.0",
    description="A CLI tool to generate standardized folder structures from templates",
    author="Cline Team",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "openai>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "onboard-project=cli_onboarding_agent.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
