import os
import pathlib
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logger():
    """
    Initializes a logger for the 'pickforme' module.
    
    This function sets up a logger for the 'pickforme' module. It creates a logger named 'pickforme' and configures it to log messages at the DEBUG level. It also creates a TimedRotatingFileHandler to log messages to a file named 'pickforme.log' located in the 'logs' directory. The handler is set to log messages at the DEBUG level. The formatter is set to log messages in the format '%(asctime)s %(levelname)8s %(funcName)25s --> %(message)s'. The logger is configured to rotate log files daily and retain 25 backups.
    
    Returns:
        log_config (logging.Logger): The logger for the 'pickforme' module
    """
    log_config = logging.getLogger('pickforme')
    log_config.setLevel(logging.DEBUG)

    # Create handlers
    project_install_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(project_install_path, 'logs')
    print('logs idr = ', logs_dir)
    pathlib.Path(logs_dir).mkdir(parents=True, exist_ok=True)
    log_file_path = os.path.join(logs_dir, 'pickforme.log')
    file_handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=25)

    # Set logging levels
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add them to handlers
    file_format = logging.Formatter('%(asctime)s %(levelname)8s %(funcName)25s --> %(message)s')
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    log_config.addHandler(file_handler)

    return log_config

# Initialize the logger
logger = setup_logger()
