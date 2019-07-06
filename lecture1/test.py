#import flask
from flask import Flask
# define app
app = Flask(__name__)

# define home page route /
@app.route("/")
def home():
    return "Home"
app.run()