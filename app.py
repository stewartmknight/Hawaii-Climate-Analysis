from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import pandas as pd



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station



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
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
        f"""<body bgcolor="mediumseagreen">"""
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation"""
    # Query all passengers
    results = session.query(Measurement.prcp, Measurement.date).all()

    # df = pd.DataFrame(results)

    prcp_dict_list = []

    for prcp, date in results:
        prcp_dict = {}
        prcp_dict[date] = prcp 
        prcp_dict_list.append(prcp_dict)

    session.close()

    # Convert list of tuples into normal list
    # all_prcp = list(np.ravel(results))

    return jsonify(prcp_dict_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station names from the database."""
    # Query all stations
    results = session.query(Station.station, Station.name, 
    Station.longitude, Station.latitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station, name, longitude, latitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitiude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperatures"""
    # Query all temperatures in the last year of the database:
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').all()

    ###NOTE: If I was going to make it for the past current year (2018-2019), 
    # I would have set the start_date to DateTime.Now and the end_date to 
    # DateTime.Now.AddYears(-1). I would have coded that but the database
    # only goes until 08-23-2017.

    tobs_dict_list = []

    for tobs, date in results:
        tobs_dict = {}
        tobs_dict[date] = tobs 
        tobs_dict_list.append(tobs_dict)

    session.close()



    return jsonify(tobs_dict_list)


@app.route("/api/v1.0/<start>")
def weather_short(start):

    session = Session(engine)

    # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
    # and return the minimum, average, and maximum temperatures for that range of dates
    def calc_temps(start_date, end_date):
        """TMIN, TAVG, and TMAX for a list of dates.
    
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
        
        Returns:
            TMIN, TAVE, and TMAX
        """
        minimum = func.min(Measurement.tobs)
        average = func.avg(Measurement.tobs)
        maximum = func.max(Measurement.tobs)
        return session.query(minimum, average, maximum).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    results = calc_temps(start, '2017-08-23')
    print(results)

    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    new_weather = []
    for result in results:
        weather_dict = {}
        weather_dict["TMIN"] = result[0]
        weather_dict["TAVG"] = result[1]
        weather_dict["TMAX"] = result[2]
        new_weather.append(weather_dict)

    return jsonify(new_weather)



@app.route("/api/v1.0/<start>/<end>")
def weather_long(start, end):

    session = Session(engine)

    # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
    # and return the minimum, average, and maximum temperatures for that range of dates
    def calc_temps(start_date, end_date):
        """TMIN, TAVG, and TMAX for a list of dates.
    
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
        
        Returns:
            TMIN, TAVE, and TMAX
        """
        minimum = func.min(Measurement.tobs)
        average = func.avg(Measurement.tobs)
        maximum = func.max(Measurement.tobs)
        return session.query(minimum, average, maximum).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    results = calc_temps(start, end)
    print(results)

    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_weather = []
    for result in results:
        weather_dict = {}
        weather_dict["TMIN"] = result[0]
        weather_dict["TAVG"] = result[1]
        weather_dict["TMAX"] = result[2]
        all_weather.append(weather_dict)

    return jsonify(all_weather)



if __name__ == '__main__':
    app.run(debug=True)
