import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, redirect, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)


@app.route("/")
def home():
	print("Server received request for 'Home' page.")
	return ("Welcome to the Surfs Up Weather API!<br><br>"
		f"Available Routes:<br>"
		f"/api/v1.0/precipitation<br>"
		f"/api/v1.0/Station<br>"
		f"/api/v1.0/tobs<br>"
		f"/api/v1.0/(Y-M-D)<br>"
		f"/api/v1.0(start=Y-M-D)/(end=Y-M-D)<br>"
	)

@app.route("/api/v1.0/precipitation")
def precipitation():
	
	results = session.query(Measurement).all()
	session.close()

	year_prcp = []
	for result in results:
		year_prcp_dict = {}
		year_prcp_dict["date"] = result.date
		year_prcp_dict["prcp"] = result.prcp
		year_prcp.append(year_prcp_dict)

	return jsonify(year_prcp)


@app.route("/api/v1.0/Station")
def stations():
	
	results = session.query(Station.station).all()
	session.close()
	all_station = list(np.ravel(results))
	return jsonify(all_station)


@app.route("/api/v1.0/tobs")
def temperature():
	
	Last_Year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	temperature_results = session.query(Measurement.tobs).filter(Measurement.date > Last_Year).all()
	session.close()
	temperature_list = list(np.ravel(temperature_results))
	return jsonify(temperature_list)


@app.route("/api/v1.0/<start>")
def single_date(start):

	Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")
	summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date >= Start_Date).all()
	session.close() 
	summary = list(np.ravel(summary_stats))
	return jsonify(summary)


@app.route("/api/v1.0/<start>/<end>")
def trip_dates(start,end):

	Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")
	End_Date = dt.datetime.strptime(end,"%Y-%m-%d")
	summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date.between(Start_Date,End_Date)).all()
	session.close()    
	summary = list(np.ravel(summary_stats))
	return jsonify(summary)

if __name__ == "__main__":
	app.run(debug=True)