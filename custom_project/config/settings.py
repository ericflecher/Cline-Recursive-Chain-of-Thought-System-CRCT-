"""
Configuration settings for {{package_name}}.
"""

# Default configuration
DEFAULT_CONFIG = {
    "debug": False,
    "log_level": "INFO",
    "timeout": 30,
    # Add your configuration settings here
}


def get_config():
    """Get the configuration settings."""
    return DEFAULT_CONFIG.copy()
