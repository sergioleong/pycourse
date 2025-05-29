from flask import Flask,render_template

# Create an instance of the Flask class
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index_01.html')