from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    return "Hello, this is a simple web page!"