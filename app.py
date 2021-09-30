#import dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Set up the Database
#1.Access SQLite database
engine=create_engine('sqlite:///hawaii.sqlite')  #this code will allow you to access the SQLite database

#2.Reflect the database into our classes
Base=automap_base()
Base.prepare(engine, reflect=True)

#3.Create a variable for each class to reference them later
Measurement=Base.classes.measurement
Station=Base.classes.station

#4.Finally, create a session link from Python to our database:
session=Session(engine)

#Set Up Flask
#1.define a flask app:
app=Flask(__name__)

#2.Create the Welcome Route
#when Creating a flask route, we must define what our route will be, we want our welcome route to be the root
#NB: images, videos, news, maps are routes in Google and Google homepage is essentially the root
#All of your routes should go after the app=Flask(__name__) line of code.

#let's define the welcome route
@app.route("/")   #Now our root or welcome route is set up, now we need to add the routing info for each of other routes.
def welcome():    
    return('''      
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
#We just added the prcp, stations, tobs and temp routes that we'll need for this module into our return statement,
#we'll use f-strings to display them for our investors

#if we navigate via terminal to our directory and type: run flask
#then copy and paste our web address into our web browser, we'll be able to see our second Flask route

#Next, we'll split up the code we wrote for the temperature analysis, precipitation analysis, and station analysis, 
#and apply it to the respective routes. Let's start with the precipitation route.

#PRECIPITATION
#let's create the prcp route
@app.route("/api/v1.0/precipitation")

#let's create the precipitation() function
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
    #we wanna create a dictionnary with the date as the key and prcp as value: we will use "jsonify"
    # jsonify converts the dictionnary to a JSON file

#NB: .\ is used to signify that we want our query to continue on the next line


#STATION ROUTE
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
#unraveling our results into a 1 dimensional array: np,ravel() and convert into a list

#MONTHLY TEMPERATURE ROUTE
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#STATISTICS ROUTE
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")     #we will have to provide both stating and ending dates

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)