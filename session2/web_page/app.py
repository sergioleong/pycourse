from flask import Flask,render_template, redirect, url_for, session, flash, request, jsonify
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv('.env')

# Import security utilities for password hashing
from werkzeug.security import generate_password_hash, check_password_hash
# Import timedelta for session lifetime management
from datetime import timedelta, datetime

# Import SQLAlchemy components and User model from our new models.py file
from models import get_db_session, close_db_session, User, engine, Base, Chat, ChatMessage
from sqlalchemy.exc import IntegrityError # For handling unique constraint violations
from sqlalchemy import desc # For ordering queries
import json # For loading bot configurations from JSON file


# Import chatbot functions from our new chatbot.py file
from chatbot import get_ollama_response

# Create an instance of the Flask class
app = Flask(__name__)

# Set the secret key for session management from the environment variable
app.secret_key = os.getenv('SECRET_KEY')

# Set the permanent session lifetime (e.g., 31 days for "remember me")
app.permanent_session_lifetime = timedelta(days=31)

# Register the close_db_session function to be called after each request
app.teardown_appcontext(close_db_session)

# --- Bot Configuration Loading ---
BOTS_CONFIG_FILE = 'bots.json'
BOTS = {} # Dictionary to store bot configurations

def load_bot_configurations():
    """Loads bot configurations from the BOTS_CONFIG_FILE."""
    global BOTS
    try:
        with open(BOTS_CONFIG_FILE, 'r') as f:
            BOTS = json.load(f)
        print(f"Loaded {len(BOTS)} bot configurations from {BOTS_CONFIG_FILE}")
    except FileNotFoundError:
        print(f"Error: {BOTS_CONFIG_FILE} not found. Please create it.")
        BOTS = {} # Ensure BOTS is an empty dict if file not found
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {BOTS_CONFIG_FILE}. Check file format.")
        BOTS = {} # Ensure BOTS is an empty dict if JSON is invalid

# Load bots when the application starts
with app.app_context():
    load_bot_configurations()

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
    """
    The main index page, showing a list of open chats and available bots.
    """
    user_id = session.get('user_id')
    db_session = get_db_session()

    # Fetch all chats for the current user, ordered by last message
    user_chats = db_session.query(Chat).filter_by(user_id=user_id, is_archived=False)\
                                       .filter(Chat.message_count > 0)\
                                       .order_by(desc(Chat.last_message_at))\
                                       .all()

    # Prepare chat data for the template, including bot name
    chats_for_display = []
    for chat in user_chats:
        bot_info = BOTS.get(chat.bot_id, {'name': 'Unknown Bot'})
        # Try to get the first user message content or use a default name
        first_message_content = "New Chat"
        if chat.messages and chat.messages[0].role == 'user':
             first_message_content = chat.messages[0].content
        elif chat.messages: # Fallback if first message is AI's (unlikely in this flow)
            first_message_content = f"Chat with {bot_info['name']}"

        chats_for_display.append({
            'id': chat.id,
            'bot_name': bot_info['name'],
            'last_message_at': chat.last_message_at.strftime('%Y-%m-%d %H:%M:%S'),
            'message_count': chat.message_count,
            'title': first_message_content # Use first message or default as title
        })

    # Pass all bot configurations to the template
    available_bots = BOTS

    return render_template('index.html',
                           username=session.get('username'),
                           user_chats=chats_for_display,
                           available_bots=available_bots)

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
    return render_template('login.html')

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
    return render_template('register.html')

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
    
    chat_id_param = request.args.get('id', type=int)
    bot_id_param = request.args.get('bot')
    
    current_chat = None
    chat_history = []
    selected_bot_id = 'default' # Default bot fallback

    # 1. Handle starting a new chat with a specific bot (creates chat and redirects)
    if bot_id_param:
        if chat_id_param:
            return redirect(url_for('chat', id=chat_id_param))

        if bot_id_param not in BOTS:
            flash(f"Bot '{bot_id_param}' not found.", 'danger')
            abort(404)

        # Create a new chat instance immediately
        new_chat = Chat(user_id=user_id, bot_id=bot_id_param, message_count=0, last_message_at=datetime.utcnow(), is_archived=False)
        db_session.add(new_chat)
        try:
            db_session.commit()
            flash(f"Started a new chat with {BOTS[bot_id_param]['name']}!", 'success')
            # Redirect to the chat page with the new chat's ID
            return redirect(url_for('chat', id=new_chat.id))
        except Exception as e:
            db_session.rollback()
            flash(f"Error creating new chat: {e}", 'danger')
            return redirect(url_for('index')) # Redirect to index on error

    # 2. Handle continuing an existing chat (requires 'id' parameter)
    elif chat_id_param:
        current_chat = db_session.query(Chat).get(chat_id_param)
        if not current_chat or current_chat.user_id != user_id:
            flash('Invalid chat ID or chat does not belong to you.', 'danger')
            abort(404) # Abort with 404 for security/correctness

        actual_bot_id = current_chat.bot_id
        chat_history = [{'role': msg.role, 'content': msg.content}
                        for msg in current_chat.messages]
        # Pass chat_id to the template so JS can use it for API calls
        selected_chat_id = current_chat.id

    # 3. If no valid 'id' or 'bot' param, redirect to the portal
    else:
        return redirect(url_for('index'))


    # Get bot configuration for the actual bot_id used in the chat
    bot_config = BOTS.get(actual_bot_id, BOTS.get('default', {}))
    bot_name = bot_config.get('name', 'AI Assistant')
    welcome_message = bot_config.get('welcome_message', 'Hello! How can I help you today?')

    return render_template('chat.html',
                           username=username,
                           chat_history=chat_history,
                           bot_name=bot_name,
                           welcome_message=welcome_message,
                           chat_id=selected_chat_id,
                           available_bots=BOTS) # Pass chat_id to the template

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """
    Handles chat requests from the frontend, saving conversation memory to the database.
    Expects 'chat_id' in the JSON payload.
    """
    print(request.json)
    user_message_content = request.json.get('message')
    chat_id = request.json.get('chat_id') # Get chat_id from JSON payload
    if not user_message_content:
        return jsonify({"error": "No message provided"}), 400
    if not chat_id:
        return jsonify({"error": "Chat ID not provided"}), 400
    # Ensure chat_id is an integer after retrieval (it should be if passed correctly from JS)
    try:
        chat_id = int(chat_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid chat ID format."}), 400

    user_id = session.get('user_id')
    db_session = get_db_session()

    current_chat = db_session.query(Chat).get(chat_id)

    # Validate chat exists and belongs to the user
    if not current_chat or current_chat.user_id != user_id:
        return jsonify({"error": "Invalid chat ID or chat does not belong to you."}), 403

    # Get bot configuration using the bot_id stored in the current_chat
    bot_config = BOTS.get(current_chat.bot_id, BOTS.get('default', {}))
    bot_model = bot_config.get('model', 'llama3') # Fallback model
    system_prompt = bot_config.get('system_prompt', "You are a helpful AI assistant.")

    # Reconstruct messages list for Ollama, including the system prompt and new user message
    messages_for_ollama = [{'role': 'system', 'content': system_prompt}]
    if current_chat.messages:
        # Only add existing messages if they are not the system prompt
        # We also need to filter out initial AI welcome messages if they were added as history (though current flow avoids this)
        for msg in current_chat.messages:
            messages_for_ollama.append({'role': msg.role, 'content': msg.content})

    # Add the current user message to the list for Ollama
    messages_for_ollama.append({'role': 'user', 'content': user_message_content})

    # Call the get_ollama_response function with the full history and the bot's model
    ai_response_content, status_code, error_message = get_ollama_response(messages_for_ollama, bot_model)

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

@app.route('/archive_chat', methods=['POST'])
@login_required
def archive_chat():
    """
    Marks a chat as archived in the database.
    Expects 'chat_id' in the JSON payload.
    """
    chat_id = request.json.get('chat_id')

    if chat_id is None:
        return jsonify({"error": "Chat ID not provided"}), 400

    user_id = session.get('user_id')
    db_session = get_db_session()

    try:
        chat_id = int(chat_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid chat ID format."}), 400

    current_chat = db_session.query(Chat).get(chat_id)

    if not current_chat or current_chat.user_id != user_id:
        return jsonify({"error": "Invalid chat ID or chat does not belong to you."}), 403

    current_chat.is_archived = True
    db_session.commit()
    flash('Chat archived successfully!', 'success')
    return jsonify({"success": True, "redirect_url": url_for('index')})

@app.route('/archived_chats')
@login_required
def archived_chats():
    """
    Displays a list of chats that have been archived by the user.
    """
    user_id = session.get('user_id')
    db_session = get_db_session()

    # Fetch all chats for the current user that ARE archived
    user_archived_chats = db_session.query(Chat).filter_by(user_id=user_id, is_archived=True)\
                                       .filter(Chat.message_count > 0)\
                                       .order_by(desc(Chat.last_message_at))\
                                       .all()

    chats_for_display = []
    for chat in user_archived_chats:
        bot_info = BOTS.get(chat.bot_id, {'name': 'Unknown Bot'})
        first_message_content = "Archived Chat"
        if chat.messages and chat.messages[0].role == 'user':
             first_message_content = chat.messages[0].content
        elif chat.messages:
            first_message_content = f"Chat with {bot_info['name']}"

        chats_for_display.append({
            'id': chat.id,
            'bot_name': bot_info['name'],
            'last_message_at': chat.last_message_at.strftime('%Y-%m-%d %H:%M:%S'),
            'message_count': chat.message_count,
            'title': first_message_content
        })

    return render_template('archived_chats.html',
                           username=session.get('username'),
                           archived_chats=chats_for_display,
                           available_bots=BOTS)

@app.route('/unarchive_chat', methods=['POST'])
@login_required
def unarchive_chat():
    """
    Unmarks a chat as archived in the database, making it visible again in the main portal.
    Expects 'chat_id' in the JSON payload.
    """
    chat_id = request.json.get('chat_id')

    if chat_id is None:
        return jsonify({"error": "Chat ID not provided"}), 400

    user_id = session.get('user_id')
    db_session = get_db_session()

    try:
        chat_id = int(chat_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid chat ID format."}), 400

    current_chat = db_session.query(Chat).get(chat_id)

    if not current_chat or current_chat.user_id != user_id:
        return jsonify({"error": "Invalid chat ID or chat does not belong to you."}), 403

    current_chat.is_archived = False # Set to False to unarchive
    db_session.commit()
    flash('Chat unarchived successfully!', 'success')
    # Redirect to index to show it back in active chats
    return jsonify({"success": True, "redirect_url": url_for('index')})

        
# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(error):
    """Renders a custom 404 page."""
    return render_template('404.html'), 404
