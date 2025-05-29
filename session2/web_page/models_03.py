from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import g # Import g from Flask for request-specific storage
import os # For accessing environment variables

# Define the database URL (read from environment variable, with a fallback)
DATABASE_URL = os.getenv('DATABASE_URL')

# Create a base class for declarative models
Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    Defines the structure and relationships for user data.
    """
    __tablename__ = 'users' # Maps this class to the 'users' table in the database

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) # Stores the hashed password

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
# This will be used to create individual session instances
Session = sessionmaker(bind=engine)

def get_db_session():
    """
    Provides a SQLAlchemy session for the current request.
    The session is stored in Flask's 'g' object to reuse it.
    If a session doesn't exist for the current request, a new one is created.
    """
    if 'db_session' not in g:
        g.db_session = Session()
    return g.db_session

def close_db_session(e=None):
    """
    Closes the SQLAlchemy session at the end of the request.
    This ensures that database connections are properly released.
    """
    db_session = g.pop('db_session', None) # Retrieve and remove the session from g
    if db_session is not None:
        db_session.close() # Close the session
