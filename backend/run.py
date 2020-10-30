from flask import Flask, Response, request, render_template, jsonify
from random import *
from flask_cors import CORS
import json
#File for importing token not tracked by git
import Token

#needed to make web requests
import requests

#store the data we get as a dataframe
import pandas as pd

#mathematical operations on lists
import numpy as np

#parse the datetimes we get from NOAA
from datetime import datetime







app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")

CORS(app)
#cors = CORS(app,resources={r"/api/*": {"origins": "*"}},allow_headers={"*"})#, resources={r"/api/*": {"origins": "*"}})
#cors = (app, resources={r"/api/request": {"origins": "*"}})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route('/api/request', methods=['POST'])
def do_request():
#   print(request.get_data())
    content = request.json
    # if content.keys().contains
    if 'date' and 'city' not in content.keys():
        return "bad json"
    
    for key in content.keys():
        print('my key: {}'.format(key))
        if(key == 'date'):            
            print('we have a date {}'.format(content['date']))
            startDate = content['date'][0]
            endDate = content['date'][1]
            startDate = startDate.split('T')[0]
            endDate = endDate.split('T')[0]
            print(startDate)
            print(endDate)
        if(key == 'city'):
            print('we have a city')


    #Hardcoded station for now.
    station_id = 'GHCND:USW00023129'
    #add the access token you got from NOAA
    myToken = Token.token()
        
        
    api_call(startDate,endDate,station_id,myToken)


    return request.args;


def api_call(startDate,endDate,station_id,Token):
    dates_temp = []
    dates_prcp = []
    temps = []
    prcp = []

    #make the api call
    r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TAVG&limit=1000&stationid='+station_id+'&startdate='+startDate+'&enddate='+endDate, headers={'token':Token})
    #load the api response as a json
    d = json.loads(r.text)

    # get all items in the response which are average temperature readings
    avg_temps = [item for item in d['results'] if item['datatype']=='TAVG']
    #get the date field from all average temperature readings
    dates_temp += [item['date'] for item in avg_temps]
    #get the actual average temperature from all average temperature readings
    temps += [item['value'] for item in avg_temps]

    #initialize dataframe
    df_temp = pd.DataFrame()

    #populate date and average temperature fields (cast string date to datetime and convert temperature from tenths of Celsius to Fahrenheit)
    df_temp['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_temp]
    df_temp['avgTemp'] = [float(v)/10.0*1.8 + 32 for v in temps]

    print(df_temp)

    return




