# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
import datetime as dt
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
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperature<br/>"
        f"<br/>"
        f"Choose a date between 2010-01-01 and 2017-08-23 in YYYY-MM-DD format:<br/><br/>"
        f"/api/v1.0/&ltstart&gt <br/><br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt <br/>"
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
@app.route("/api/v1.0/<start>")
def start_date_temp(start):

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end =  dt.date(2017, 8, 23)
    temp_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end).all()
    mystart = {}
    for row in temp_query:
        mystart["Minimum Temperature: "] = row[0]
        mystart["Average Temperature: "] = row[1]
        mystart["Maximum Temperature: "] = row[2]
    return jsonify(mystart)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start,end):
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    start_end_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    mystart2 = {}
    for row in start_end_query:
        mystart2["Minimum Temperature: "] = row[0]
        mystart2["Average Temperature: "] = row[1]
        mystart2["Maximum Temperature: "] = row[2]

    return jsonify(mystart2)

if __name__ == '__main__':
    app.run(debug=True)
