import logging

# Create a logger
logger = logging.getLogger('sqlalchemy.engine')

# Set the logging level
logger.setLevel(logging.INFO)  # or DEBUG for more detail

# Create a file handler to write logs to a file
file_handler = logging.FileHandler('logs/sqlalchemy.log')
file_handler.setLevel(logging.INFO)

# Create a log formatter and attach it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)
