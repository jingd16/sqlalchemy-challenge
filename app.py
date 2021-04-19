import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    #Document the API
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Convert the query results to a dictionary using date as the key and prcp as the value. Return the result as JSON format."
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"Return a JSON list of stations from the dataset."
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Query the dates and temperature observations of the most active station for the last year of data."
        f"Return a JSON list of temperature observations (TOBS) for the previous year"
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd (example date format: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd) <br/>"
        f"Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start and end date range."
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(station.id, station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query the dates and temperature observations of the most active station for the last year of data.
    #Return a JSON list of temperature observations (TOBS) for the previous year.
    results = session.query(measurement.station, measurement.date, measurement.tobs).\
                filter(measurement.date <= '2017-08-23' ).\
                filter(measurement.date >= '2016-08-23').\
                filter(measurement.station == 'USC00519281').\
                all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

    all_data = list(np.ravel(results))

    return jsonify(all_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()

    all_data = list(np.ravel(results))

    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True)
