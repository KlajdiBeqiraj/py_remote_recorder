"""
This module provides a utility function to configure and retrieve a logger
using Uvicorn's logging configuration.
"""

import logging
import logging.config

import uvicorn


def get_logger():
    """
    Configures the logging using Uvicorn's logging configuration and returns a logger.

    Returns:
        logging.Logger: The logger instance configured using Uvicorn's settings.
    """
    # Get Uvicorn's default logging configuration
    log_config = uvicorn.config.LOGGING_CONFIG

    # Apply the logging configuration
    logging.config.dictConfig(log_config)

    # Retrieve and return the Uvicorn logger
    logger = logging.getLogger("uvicorn")
    return logger
