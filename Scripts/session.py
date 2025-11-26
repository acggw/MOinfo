import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/sqlalchemy.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Ensure folder exists
DB_FOLDER = "database"
os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = f"{DB_FOLDER}/database.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
Session = sessionmaker(bind=engine)
