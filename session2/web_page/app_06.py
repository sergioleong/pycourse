from flask import Flask,render_template, redirect, url_for, session, flash, request, jsonify
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv('.env_06')

# Import security utilities for password hashing
from werkzeug.security import generate_password_hash, check_password_hash
# Import timedelta for session lifetime management
from datetime import timedelta, datetime

# Import SQLAlchemy components and User model from our new models.py file
from models_06 import get_db_session, close_db_session, User, engine, Base, Chat, ChatMessage
from sqlalchemy.exc import IntegrityError # For handling unique constraint violations
from sqlalchemy import desc # For ordering queries


# Import chatbot functions from our new chatbot.py file
from chatbot_05 import get_ollama_response

# Create an instance of the Flask class
app = Flask(__name__)

# Set the secret key for session management from the environment variable
app.secret_key = os.getenv('SECRET_KEY')

# Set the permanent session lifetime (e.g., 31 days for "remember me")
app.permanent_session_lifetime = timedelta(days=31)

# Register the close_db_session function to be called after each request
app.teardown_appcontext(close_db_session)

# --- Helper function for authentication check ---
def login_required(f):
    """
    A decorator to protect routes that require a logged-in user.
    If no user is in the session, it redirects to the login page.
    """
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
    
# --- Flask Routes ---
# Define the route for the home page
@app.route('/')
@login_required
def index():
    return redirect(url_for('chat'))

# Define the route for the login page, handling both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    - GET request: Displays the login form.
    - POST request: Processes the submitted form data, authenticates the user,
      and sets the 'username' in the session upon successful login.
    """
    if session.get('username'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        remember_me = request.form.get('remember_me')
        error = None

        db_session = get_db_session()
        # Query the User model using SQLAlchemy to find the user by username
        user = db_session.query(User).filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password): # Check uername and hashed password
            error = 'Incorrect uername/password.'

        if error is None:
            session.clear()
            session['username'] = user.username
            session['user_id'] = user.id # Store user_id in session for database operations
            if remember_me:
                session.permanent = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash(error, 'danger')
    return render_template('login_03.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    - GET request: Displays the registration form.
    - POST request: Processes the submitted form data, hashes the password,
      and inserts the new user into the database using SQLAlchemy.
    """
    if session.get('username'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        error = None

        db_session = get_db_session()

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # Check if username already exists using SQLAlchemy query
        elif db_session.query(User).filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db_session.add(new_user)
            try:
                db_session.commit() # Commit the new user to the database
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            except IntegrityError:
                # This catches potential unique constraint violations if two users try to register
                # with the same username simultaneously (though less likely with prior check)
                db_session.rollback() # Rollback the transaction in case of error
                flash(f"User {username} is already registered.", 'danger')
        else:
            flash(error, 'danger')
    return render_template('register_03.html')

# Define the route for logging out
@app.route('/logout')
def logout():
    """
    Logs out the current user by removing the 'username' from the session.
    """
    # Remove the username from the session if it exists
    session.pop('username', None)
    flash('You have been logged out.', 'info') # Flash an informational message
    return redirect(url_for('index')) # Redirect to the home page

@app.route('/chat')
@login_required # Protect the chat page
def chat():
    """
    Renders the main chat interface.
    """
    username = session.get('username')
    user_id = session.get('user_id')
    db_session = get_db_session()
    
    # Find the most recent chat for the current user
    # For now, we'll assume one active chat per user or pick the latest one
    current_chat = db_session.query(Chat).filter_by(user_id=user_id)\
                                     .order_by(desc(Chat.last_message_at))\
                                     .first()

    chat_history = []
    chat_id = None
    if current_chat:
        chat_id = current_chat.id
        # Load messages associated with this chat, ordered by message_index
        chat_history = [{'role': msg.role, 'content': msg.content}
                        for msg in current_chat.messages]
    else:
        # If no chat exists, initialize with a welcome message for the frontend
        # This message won't be saved to DB until the first user message
        pass # The frontend will display a default welcome message if history is empty

    # Store the current chat_id in the session for /api/chat to use
    session['current_chat_id'] = chat_id

    return render_template('chat_06.html', username=username, chat_history=chat_history)

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """
    Handles chat requests from the frontend, saving conversation memory to the database.
    """
    user_message_content = request.json.get('message')
    if not user_message_content:
        return jsonify({"error": "No message provided"}), 400

    user_id = session.get('user_id')
    db_session = get_db_session()
    current_chat_id = session.get('current_chat_id')
    current_chat = None

    # Retrieve or create the current chat for the user
    if current_chat_id:
        current_chat = db_session.query(Chat).get(current_chat_id)

    if not current_chat:
        # If no current chat or chat_id is invalid, create a new chat for the user
        current_chat = Chat(user_id=user_id, bot_id='default', message_count=0, last_message_at=datetime.utcnow())
        db_session.add(current_chat)
        db_session.flush() # Flush to get the ID for the new chat before committing
        session['current_chat_id'] = current_chat.id # Store new chat ID in session

    # Reconstruct messages list for Ollama, including the new user message
    # This ensures Ollama gets the full context from the DB
    messages_for_ollama = []
    if current_chat.messages:
        messages_for_ollama = [{'role': msg.role, 'content': msg.content}
                               for msg in current_chat.messages]

    # Add the current user message to the list for Ollama
    messages_for_ollama.append({'role': 'user', 'content': user_message_content})

    # Call the get_ollama_response function from the chatbot module with the full history
    ai_response_content, status_code, error_message = get_ollama_response(messages_for_ollama)

    if error_message:
        db_session.rollback() # Rollback if AI response failed
        return jsonify({"error": error_message}), status_code
    else:
        # Save user message to database
        user_message_db = ChatMessage(
            chat_id=current_chat.id,
            message_index=current_chat.message_count,
            role='user',
            content=user_message_content,
            timestamp=datetime.utcnow()
        )
        db_session.add(user_message_db)
        current_chat.message_count += 1
        current_chat.last_message_at = datetime.utcnow()

        # Save AI message to database
        ai_message_db = ChatMessage(
            chat_id=current_chat.id,
            message_index=current_chat.message_count,
            role='assistant',
            content=ai_response_content,
            timestamp=datetime.utcnow()
        )
        db_session.add(ai_message_db)
        current_chat.message_count += 1
        current_chat.last_message_at = datetime.utcnow()

        db_session.commit() # Commit all changes to the database
        return jsonify({"response": ai_response_content})

