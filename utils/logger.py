"""Logging configuration for the application."""
import logging
import sys

def setup_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    Set up and return a logger with simple console output (no timestamp).
    
    :param name: Logger name
    :param level: Logging level
    :return: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding multiple handlers if logger already exists
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        # Simple format without date/time
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
