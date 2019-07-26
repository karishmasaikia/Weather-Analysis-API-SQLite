
# coding: utf-8

# In[16]:


# 1. import Flask
from flask import Flask,jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[7]:


engine = create_engine("sqlite:///hawaii.sqlite")


# In[8]:


Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()


# In[9]:


Station=Base.classes.stations
Measurement= Base.classes.measurements
session=Session(engine)


# In[11]:


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# In[52]:


@app.route("/")
def welcome_home():
    print("Server received request for 'Home' page...") 
    return (f"Welcome to my Weather Analysis page for Hawaii!<br/>"
        f"Available Routes:<br/>"
        f"Temperature obs with dates for last year : /api/v1.0/precipitation<br/>"
        f"Station List : /api/v1.0/stations<br/>"
        f"Temperature observation for last year : /api/v1.0/tobs<br/>"
        f"Temp min, max and avg query with start date only (will return Temp Min, Max Avg respectively) : /api/v1.0/<start><br/>"
        f"Temp min, max and avg query with start & end date (will return Temp Min, Max Avg respectively): /api/v1.0/<start>/<end>"
        
    )


# In[28]:


@app.route("/api/v1.0/precipitation")
def precipitation():
    #Query for the dates and temperature observations from the last year.
    year_ago_date = dt.date.today() - dt.timedelta(days=365)
    Temp_obs_last_year=session.query(Measurement.date,func.avg(Measurement.tobs)).    filter(Measurement.date > year_ago_date).group_by(Measurement.date).order_by(Measurement.date).all()
    
    #Convert the query results to a Dictionary using date as the key and tobs as the value.
    Temp_obs_lastyear_dict={}
    Temp_obs_lastyear_list=[]
    i=0
    for values in Temp_obs_last_year:
        Temp_obs_lastyear_dict[Temp_obs_last_year[i][0]]=Temp_obs_last_year[i][1]
        Temp_obs_lastyear_list.append(Temp_obs_lastyear_dict)
        i=i+1
        
    #Return the json representation of your dictionary
    return jsonify(Temp_obs_lastyear_list)
    


# In[48]:


@app.route("/api/v1.0/stations")
def stations():
    #Return a json list of stations from the dataset
    Stations=session.query(Station.name).all()
    Stations_ravel=list(np.ravel(Stations))
    return (jsonify(Stations_ravel))


# In[51]:


@app.route("/api/v1.0/tobs")
#Return a json list of Temperature Observations (tobs) for the previous year
def Temp_obs_lastyear():
    year_ago_date = dt.date.today() - dt.timedelta(days=365)
    Temp_obs_last_year=session.query(Measurement.tobs).    filter(Measurement.date > year_ago_date).all()
    
    Temp_obs_last_year_format=list(np.ravel(Temp_obs_last_year))
    return (jsonify(Temp_obs_last_year_format))
    
    


# In[58]:


@app.route("/api/v1.0/<start>")
def start_date():
    start_date_lastyear=(dt.datetime.strptime(start, '%Y-%m-%d'))-dt.timedelta(days=365)
    
    TMIN=session.query(func.avg(Measurement.tobs)).filter(Measurement.date >=start_date_lastyear).        group_by(Measurement.date).order_by(func.avg(Measurement.tobs)).first()
        
    TMAX=session.query(func.avg(Measurement.tobs)).filter(Measurement.date >=start_date_lastyear).        group_by(Measurement.date).order_by(func.avg(Measurement.tobs).desc()).first()
    
    TAVG=session.query(func.avg(Measurement.tobs)).filter(Measurement.date >=start_date_lastyear).all()
    
    
    return (TMIN,TMAX,TAVG)
    


# In[60]:


@app.route("/api/v1.0/<start>/<end>")
def start_date_and_end_date():
    start_date_lastyear=(dt.datetime.strptime(start, '%Y-%m-%d'))-dt.timedelta(days=365)
    end_date_lastyear=(dt.datetime.strptime(end, '%Y-%m-%d'))-dt.timedelta(days=365)
    
    TMIN=session.query(func.avg(Measurement.tobs)).filter(Measurement.date >=start_date_lastyear).    filter(Measurement.date <= end_date_lastyear).    group_by(Measurement.date).order_by(func.avg(Measurement.tobs)).first()
        
    TMAX=session.query(func.avg(Measurement.tobs)).filter(Measurement.date >=start_date_lastyear).    filter(Measurement.date <= end_date_lastyear).    group_by(Measurement.date).order_by(func.avg(Measurement.tobs).desc()).first()
    
    TAVG=session.query(func.avg(Measurement.tobs)).filter(Measurement.date >=start_date_lastyear).    filter(Measurement.date <= end_date_lastyear).all()
    
    
    return (TMIN,TMAX,TAVG)


# In[ ]:


if __name__ == "__main__":
    app.run(debug=True)

