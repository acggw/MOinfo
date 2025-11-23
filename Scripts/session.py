import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure folder exists
DB_FOLDER = "database"
os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = f"{DB_FOLDER}/database.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Session factory
Session = sessionmaker(bind=engine)
