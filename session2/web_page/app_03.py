from flask import Flask,render_template, redirect, url_for, session, flash, request
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv('.env_03')

# Import security utilities for password hashing
from werkzeug.security import generate_password_hash, check_password_hash
# Import timedelta for session lifetime management
from datetime import timedelta

# Import SQLAlchemy components and User model from our new models.py file
from models_03 import get_db_session, close_db_session, User, engine, Base
from sqlalchemy.exc import IntegrityError # For handling unique constraint violations


# Create an instance of the Flask class
app = Flask(__name__)

# Set the secret key for session management from the environment variable
app.secret_key = os.getenv('SECRET_KEY')

# Set the permanent session lifetime (e.g., 31 days for "remember me")
app.permanent_session_lifetime = timedelta(days=31)

# Register the close_db_session function to be called after each request
app.teardown_appcontext(close_db_session)

# Define the route for the home page
@app.route('/')
def index():
    # Get the username from the session, default to None if not logged in
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('index_03.html', username=username)

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
