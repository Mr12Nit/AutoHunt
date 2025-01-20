import logging
from typing import Optional

def setup_logger(logger_name: str, log_file: Optional[str] = None, log_level: int = logging.DEBUG) -> logging.Logger:
    """
    Sets up a logger with both console and optional file logging.

    Args:
        logger_name (str): The name of the logger.
        log_file (Optional[str]): The file to log messages to. If None, no file logging is configured.
        log_level (int): The logging level (e.g., logging.DEBUG, logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create or get a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)  # Set the logger level

    # Check if the logger already has handlers (to avoid duplicate logs)
    if not logger.handlers:
        # Create a log message formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Add file handler if a log file is provided
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # Create a console (stream) handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
