# Import the dependencies.
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask , jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the database schema tables

Base = automap_base()
Base.prepare(engine)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Binding session between python app and database 
session = Session(engine)

app = Flask(__name__)

# Displaying available routes on the landing apge

@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii CLimate Analysis API <br/>"
        f"Available Routes:<br/>"
        f"/api/V1.0/precipitaion<br/>"
        f"/api/V1.0/station<br/>"
        f"/api/V1.0/tobs<br/>"
        f"/api/V1.0/temp/start<br/>"
        f"/api/V1.0/temp/start/end<br/>"
        f" <p> 'start' and 'end' date should be in the format MMDDYYYY.</p>"

    )
# Static routes 

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

    session.close()
    precip = {date : prcp for date, prcp in precipitation}

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return json(stations=stations)

@app.route("/api/v1.0/tobs") 
def temp_monthly():
    prev_year = st.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= prev_year).all()

    print()

    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)

# Dynamic routes 

@app.route("/api.v1.0/temp/<start>")

@app.route("/api.v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
        
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
        filter(Measurement.date >= start).all()

        session.close()

        temps = list(np.ravel(results))
        return jsonify(temps=temps) 

    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    print(start)
    print(end)
    print(results)
    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)


if __name__ == "__main__":
    app.run(debug=True)



