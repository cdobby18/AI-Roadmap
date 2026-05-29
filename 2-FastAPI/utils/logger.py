"""
Utility functions and configurations
"""

import logging
from typing import Optional

# ================================
# LOGGER SETUP
# ================================

def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Usage:
        logger = get_logger(__name__)
        logger.info("Processing request")
        logger.error("An error occurred", exc_info=True)
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger


# ================================
# COMMON UTILITIES
# ================================

def is_valid_email(email: str) -> bool:
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def truncate_string(s: str, length: int = 50) -> str:
    """Truncate string to specified length"""
    return s[:length] + "..." if len(s) > length else s
