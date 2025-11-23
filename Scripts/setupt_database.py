from session import engine
from tables import Base

def create_database():
    print("Creating database and tables...")
    Base.metadata.create_all(engine)
    print("Done!")

if __name__ == "__main__":
    create_database()