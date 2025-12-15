import os

DB_FOLDER = "database"
folder_path = os.path.abspath("database")
DATABASE_URL = f"sqlite:///{folder_path}/database.db"
#print(DATABASE_URL)
DATABASE_LOCATION = "database/database.db"