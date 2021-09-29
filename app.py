#import flask
from flask import Flask

#Create a new Flask app instance
app = Flask(__name__)

#Create Flask routes
##First we need to define the staring point also known as Root
@app.route('/')
def hello_world():            #Whenever you make a route in Flask, you put the code you want in that specific route below @app.route('/')
    return 'Hello world'
#We just created our first flask route

#How to Run a flask App
#1st we need to navigate from terminal to the folder where we've saved our code