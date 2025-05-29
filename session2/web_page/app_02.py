from flask import Flask,render_template, redirect, url_for, session, flash, request
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv('.env_02')

# Create an instance of the Flask class
app = Flask(__name__)

# Set the secret key for session management from the environment variable
app.secret_key = os.getenv('SECRET_KEY', 'default_fallback_secret_key')

# Dictionary to store user credentials
users = {
    "test": os.getenv('TEST_USER_PASSWORD', 'test')
}


# Define the route for the home page
@app.route('/')
def index():
    # Get the username from the session, default to None if not logged in
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('index_02.html', username=username)

# Define the route for the login page, handling both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    - GET request: Displays the login form.
    - POST request: Processes the submitted form data, authenticates the user,
      and sets the 'username' in the session upon successful login.
    """
    if request.method == 'POST':
        # Retrieve form data from the request
        username = request.form['username'].strip()  # Strip whitespace from username
        password = request.form['password'].strip()  # Strip whitespace from password

        # Basic authentication: Check if username and password match our dummy data
        if username in users and users[username] == password:
            # If credentials are valid, store the username in the session
            session['username'] = username
            flash('Logged in successfully!', 'success') # Flash a success message
            username2 = session.get('username')
            
            return redirect(url_for('index')) # Redirect to the home page
        else:
            # If credentials are invalid, flash an error message
            flash('Invalid username or password.', 'danger')
    return render_template('login_02.html')

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
