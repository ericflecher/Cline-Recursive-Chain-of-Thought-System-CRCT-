#!/usr/bin/env python
"""
Script to run the my_awesome_project package.
"""

import argparse
import sys
from my_awesome_project import main


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run my_awesome_project")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    return parser.parse_args()


def main_cli():
    """Run the main CLI function."""
    args = parse_args()
    if args.verbose:
        print("Verbose mode enabled")
    main.run()
    return 0


if __name__ == "__main__":
    sys.exit(main_cli())
