
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from flask import g # Import g from Flask for request-specific storage
import os # For accessing environment variables
from datetime import datetime # For handling datetime objects

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

    # Define a relationship to the Chat model
    # 'backref' creates a 'user' attribute on Chat objects, linking back to the User
    chats = relationship('Chat', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Chat(Base):
    """
    SQLAlchemy model for the 'chats' table.
    Represents a single conversation.
    """
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bot_id = Column(String, nullable=False, default='default')
    message_count = Column(Integer, nullable=False, default=0)
    last_message_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Define a relationship to the ChatMessage model
    # 'order_by' ensures messages are retrieved in chronological order
    # 'cascade="all, delete-orphan"' ensures messages are deleted when the chat is deleted
    messages = relationship('ChatMessage', backref='chat', lazy=True, order_by='ChatMessage.message_index', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chat(id={self.id}, user_id={self.user_id}, bot_id='{self.bot_id}')>"

class ChatMessage(Base):
    """
    SQLAlchemy model for the 'chat_history' table.
    Represents a single message within a conversation.
    """
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    message_index = Column(Integer, nullable=False) # For ordering messages within a chat
    role = Column(String, nullable=False) # 'user' or 'assistant'
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, chat_id={self.chat_id}, role='{self.role}', index={self.message_index})>"


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
