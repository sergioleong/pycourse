# Introduction
In this guide, we'll walk you through the process of building a Flask web application that integrates a database and connects to remote AI services. Our project is a personalized chatbot portal, allowing users to securely interact with various AI models, manage their conversations, and revisit chat histories.

You'll see how to set up a Flask server, manage user authentication, handle persistent chat data with a database, and communicate with an external AI service to generate responses. This README will cover the key steps and code snippets from each phase of development, focusing specifically on the Python backend logic.

# Pip Requirements
    - flask

# Phase 0 - Set Up Flask Server
New files:
    app_00.py

We'll start by establishing the core of our web application: the Flask server. This phase covers the basic Flask setup, including creating the application instance, managing configuration, and defining initial routes.

We start loading flask module and creating our app instance with:
    from flask import Flask
    app = Flask(__name__)

Then we define our first route as the function home. This function for now will simply return a text message:
    def home():
        return "Hello, this is a simple web page!"

Then, we add the decorator "route" to tell flask to use this function when serving our main page:
    @app.route('/')
    def home():

Now, we can start our server with :
    flask --app app_<version> --debug run
We can access it from the default page:
    http://127.0.0.1:5000/

    
# Phase 1 - Templates
New files:
    app_01.py
    /templates/index_01.html

In this phase, we move beyond simple string responses and introduce Jinja2 templates to build richer HTML pages. This separation of concerns—Python handling logic and Jinja rendering HTML—is crucial for maintaining larger web applications.

First we create our index.html template under /templates folder. This page is basically a html that will be our template for the main page.

Now, in order to use our templates we need to add a new import from the Flask module:
    render_template : method used to render Jinja2 templates from under the /templates folder

Then we can simply update our home function to render this template instead of returning a txt message:
    def home():
        return render_template('index.html')

Latter we will see that we can set some variables when rendering templates, but we won't enter in detail on these templates. For more information you can check Jinja2 templates online.


# Phase 2 - Simple loggin
New files:
    app_02.py
    .env_02
    /templates/index_02.html
    /templates/login_02.html

In this phase, we introduce basic user authentication and session management to control access to our application. This allows users to log in and out, maintaining their state across different requests.

First, from now on we are going to use environment files to store our configurations. For that we are going to store our .env file with dotenv as we have seen in the previous session.

Now, we need to import few new modules from Flask:
    redirect: Redirects the user to a different URL.
    url_for: Dynamically build URLs for specific functions.
    session: Flask's built-in object for managing user sessions. 
    flash: Used to display one-time messages to the user (e.g., "Logged in successfully!"). These messages are stored in the session and retrieved on the next request, then cleared.
    request: An object that holds all incoming request data, such as form submissions (request.form), query parameters (request.args), and JSON payloads (request.json).

First, to keep our user logged, we will configure flask sessions.
In order to use them, we need to set our application secret with:
    app.secret_key
We will get this value from the environment variables

As for our users list, for now let's simply create a static user test, and store it's password also in the environment file.

Now, first let's modify our home function (renamed to index now).
# Define the route for the home page
    @app.route('/')
    def index():
        username = session.get('username')
        if not username:
            return redirect(url_for('login'))
        return render_template('index.html', username=username)

Here we are doing 3 changes:
- We try to get the username value from session.
- If username is not set, we redirect to login using both redirect and url_for functions
otherwise we render the index page, this time sending the username as parameter.


Now we need to add 2 new methods, login and logout.

Our login function will check if the request methor is GET or POST, and in case of a POST request check if the credentials sent are correct.
To check the method, we can simply check the value of "request.method" variable. 
In a similar way, we can use "request.form" dictionary to get the parameters sent by the user.

For now we will simply do a quick check that the username sent by the user and the password for it matches the stored ones. In that case we record the username in the session dictionary and redirect our index page.
If don't match, we record the error with flash and render the login template. Same as if it's a GET request.

For our logout functon we simply pop username from session and redirect to index also.


