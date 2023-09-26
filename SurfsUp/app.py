# Import the dependencies.
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def get_precipitation_data():

    # Get the latest observation date
    max_date = session.query(func.max(Measurement.date)).first()

    # Convert it to a datetime object
    end_date = dt.datetime.strptime(max_date[0], '%Y-%m-%d')

    # Calculate a year in the past
    start_date = end_date - dt.timedelta(days=366)

    # Select date and precipitation (prcp) from the measurement table where where the observation date is in the last year 
    precip_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(start_date, end_date)).order_by(Measurement.date).all()

    # For each result, add the date as the key and precipitation as the value
    all_measurements = []
    for date, prcp in precip_results:
        measurement_dict = {}
        measurement_dict[date] = prcp
        all_measurements.append(measurement_dict)
    
    # return a list of date/precipitation key/value pairs as json
    return jsonify(all_measurements)

if __name__ == '__main__':
    app.run(debug=True)