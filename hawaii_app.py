# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session
session = Session(engine)
# Flask Setup
app = Flask(__name__)

#Routes
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate Page!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperature<br/><br/>"
        f"Enter start date in the specified format:<br/>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"<br/>"
        f"Enter start and end date in the specified format:<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        )

#Precipition totals for Aug 2016-2017
@app.route("/api/v1.0/precipitation")
def precipitation():

    results = session.query(Measurement.date, Measurement.prcp).all()
    all_prcp =[]
    for date in results:
        prcp_dict = {}
        prcp_dict["date"] = date.date
        prcp_dict["prcp"] = date.prcp
        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)

#Available climate stations
@app.route("/api/v1.0/stations")
def stations():

    station_query = session.query(Station.id, Station.station).all()
    station_dict= dict(station_query)
    return jsonify(station_dict)

#Temperature data for Aug 2016-2017
@app.route("/api/v1.0/temperature")
def tobs():

    temp_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
        order_by(Measurement.date).all()
    tobs_dict = dict(temp_query)

    return jsonify(tobs_dict)

#Temperature stats for given date
@app.route('/api/v1.0/<date>/')
def given_date(date):

    results = session.query(Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date == date).all()

    data_list = []
    for result in results:
        row = {}
        row['Date'] = result[0]
        row['Average Temperature'] = result[1]
        row['Highest Temperature'] = result[2]
        row['Lowest Temperature'] = result[3]
        data_list.append(row)

    return jsonify(data_list)

#Temperature stats for a range of dates
@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):

    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = result[0]
        row["Highest Temperature"] = result[1]
        row["Lowest Temperature"] = result[2]
        data_list.append(row)
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)
