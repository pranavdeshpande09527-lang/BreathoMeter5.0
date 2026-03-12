import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Creates a centralized logger for the application.
    Excludes sensitive data naturally by ensuring developers explicitly map what to log.
    """
    logger = logging.getLogger(name)
    
    # Only configure if no handlers exist to avoid duplicates
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        
        logger.addHandler(ch)
        
    return logger

app_logger = setup_logger("breathometer_app")
