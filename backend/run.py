from flask import Flask, Response, request, render_template, jsonify
from random import *
from flask_cors import CORS

import weather_api
import plots

import json
#File for importing token not tracked by git
import Token
#Import twitter request code.
import twitter_request

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
    #need lat, long, startDate,endDate
    content = request.json
    # get data from json
    #latitude longitude date
    if 'latitude' and 'longitude' and 'date' not in content.keys():
        return "bad json"


    startDate = content['date'][0]
    endDate = content['date'][1]
    startDate = startDate.split('T')[0]
    endDate = endDate.split('T')[0]
    lat = content['latitude']
    lon = content['longitude']



    return_data = {}
    data = weather_api.api_call(lat,lon,startDate,endDate)
    images = plots.makePlots(data)

    week_data = weather_api.parse_data(data)
    return_data['week'] = week_data
    #need:
        # maxwind_mph
        # avgtemp_f
        # maxtemp_f
        # mintemp_f
        # totalprecip_in
        # snow_in
        # avg_wind_speed
        # avghumidity
        # avg_cloud_cover_percent
    #get name of place
    city = data[startDate]['city']
    state = data[startDate]['state']
    return_data['city'] = city
    return_data['state'] = state
    #decode images for json serialization
    for i in range(len(images)):
        images[i] = images[i].decode()

    return_data['plots'] = images
    return_json = json.dumps(return_data)



    return return_json;


@app.route('/api/twitter_request', methods=['POST'])
def do_twitter_request():
    content = request.json

    query = ''
    for word in content['keywords']:
        query = query + ' ' + word
    query = query + '-filter:retweets'
    longitude = content['longitude']
    latitude = content['latitude']
    radius = content['radius']
    date = content['date']
    print(date)
    # longitude = '-87.785555'
    # latitude = '41.812925'
    # radius = '50'
    # query = 'sunny -filter:retweets'
    #date = '2020-11-16'
    json_return_value = twitter_request.get_tweets(longitude,latitude,radius,query, date)
    #print(json_return_value)
    return json_return_value
