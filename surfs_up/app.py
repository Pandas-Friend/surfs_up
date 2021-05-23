import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
app = Flask(__name__)
# define welcome route
@app.route("/")
# add routing information for each of the other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
# create rute for precipitation analysis
@app.route("/api/v1.0/precipitation")  

# create precipitation function
def precipitation():
    # Calculate date 1 year ago from most recent date 
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # write a query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # Create dictionary and jsonify it
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Define route for stations
@app.route("/api/v1.0/stations")

#Create new function called stations()
def stations():
    # Create query that will allow us to get all stations in our database
    results = session.query(Station.station).all()
    # We want to start by unraveling our results into a one-dimensional array
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Define route
@app.route("/api/v1.0/tobs")

# create a function called temp_monthly()
def temp_monthly():
    # Now, calculate the date one year ago from the last date in the database.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # unravel the results into a one-dimensional array and convert that array into a list
    temps = list(np.ravel(results))
    # jsonify our temps list
    return jsonify(temps=temps)

#  this route is different from the previous ones in that we will have to provide both a starting and ending date. Add the following code to create the routes
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Next, create a function called stats() to put our code in.
# add parameters to our stats()function: a start parameter and an end parameter
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # Since we need to determine the starting and ending date, add an if-not statement to our code.
    # This will help us accomplish a few things. We'll need to query our database using the list that we just made.
    # Then, we'll unravel the results into a one-dimensional array and convert them to a list. Finally, we will jsonify our results and return them.
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    # Now we need to calculate the temperature minimum, average, and maximum with the start and end dates.
    # We'll use the sel list, which is simply the data points we need to collect. Let's create our next query, which will get our statistics data.
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)