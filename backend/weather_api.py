
import requests
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import plots
import Token

def eval_max(old,new):
    if(old > new):
        return old
    else:
        return new

def eval_min(old,new):
    if(old < new):
        return old
    else:
        return new

def parse_data(data):
    week = {}
    maxtemp_f = -999
    maxwind_mph = 0
    mintemp_f = 999
    total_cloud_cover, total_humidity, total_wind_speed, total_snow, total_precip, total_temp = (0 for i in range(6))
    for day in data.keys():
        one_day = data[day]
        total_cloud_cover += one_day['avg_cloud_cover_percent']
        total_humidity += one_day['avghumidity']
        total_wind_speed += one_day['avg_wind_speed']
        total_snow += one_day['snow_in']
        total_precip += one_day['totalprecip_in']
        total_temp += one_day['avgtemp_f']
        maxtemp_f = eval_max(one_day['maxtemp_f'],maxtemp_f)
        maxwind_mph = eval_max(one_day['maxwind_mph'],maxwind_mph)
        mintemp_f = eval_min(one_day['mintemp_f'],mintemp_f)
        # mintemp_f
        # maxwind_mph

    num_days = len(data)
    week['avg_cloud_cover_percent'] = total_cloud_cover/num_days
    week['avghumidity'] = total_humidity/num_days
    week['avg_wind_speed'] = total_wind_speed/num_days
    week['snow_in'] = total_snow/num_days
    week['total_precip'] = total_precip
    week['avgtemp_f'] = total_temp/num_days
    week['maxtemp_f'] = maxtemp_f
    week['mintemp_f'] = mintemp_f
    week['maxwind_mph'] = maxwind_mph
            # maxwind_mph
            # avgtemp_f
            # maxtemp_f
            # mintemp_f
            # totalprecip_in
            # snow_in
            # avg_wind_speed
            # avghumidity
            # avg_cloud_cover_percent
    return week

def api_call(latitude,longitude,startDate,endDate):
    key = Token.token()

    currentDate = datetime.datetime.strptime(startDate,'%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(endDate,'%Y-%m-%d').date()
    dates = [currentDate + datetime.timedelta(days=x) for x in range((endDate-currentDate).days + 1)]
    data = {}
    for day in dates:
        day = day.strftime('%Y-%m-%d')
        r = requests.get('http://api.weatherapi.com/v1/history.json?key='+key+'&q='+str(latitude)+','+str(longitude)+'&dt='+day)
        d = json.loads(r.text)
        day_data = d['forecast']['forecastday'][0]['day']
        temp = {}
        #keep pile:
        #date
        #maxtemp_f, mintemp_f, avgtemp_f, maxwind_mph
        #totalprecip_in
        #avgvis_miles
        #avghumidity
        #condition
        temp['city'] = d['location']['name']
        temp['state'] = d['location']['region']
        temp['maxtemp_f'] = day_data['maxtemp_f']
        temp['mintemp_f'] = day_data['mintemp_f']
        temp['avgtemp_f'] = day_data['avgtemp_f']
        temp['maxwind_mph'] = day_data['maxwind_mph']
        temp['totalprecip_in'] = day_data['totalprecip_in']
        temp['avgvis_miles'] = day_data['avgvis_miles']
        temp['avghumidity'] = day_data['avghumidity']
        temp['condition'] = day_data['condition']['text']
        temp['icon'] = day_data['condition']['icon']
        snow_total = 0
        cloud_total = 0
        num_hours = 0
        wind_speed = []
        wind_dir = []
        #keep pile for hours:
        #avg cloud cover
        #snow total
        #avg wind direction
        #avg wind speed
        for hour in d['forecast']['forecastday'][0]['hour']:
            num_hours+=1
            if(hour['will_it_snow'] == 1):
                snow_total+= hour['precip_in']

            cloud_total += hour['cloud']
            wind_dir.append(hour['wind_degree'])
            wind_speed.append(hour['wind_mph'])



        temp['avg_cloud_cover_percent'] = cloud_total/num_hours
        temp['snow_in'] = snow_total
        #calculate average wind direction
        V_EW = np.empty(len(wind_dir))
        V_NS = np.empty(len(wind_dir))
        if(len(wind_dir)== len(wind_speed)):
            for i in range(len(wind_dir)):
                #calculate vectors for wind speed-dir
                V_EW[i] = wind_speed[i] * np.sin(wind_dir[i] * (np.pi/180))
                V_NS[i] = wind_speed[i] * np.cos(wind_dir[i] * (np.pi/180))
            average_wind_dir = np.arctan2(sum(V_EW),sum(V_NS)) * (180/np.pi)
            #remove negative values
            average_wind_dir = (360 + average_wind_dir) % 360

        temp['avg_wind_dir'] = average_wind_dir
        temp['avg_wind_speed'] = sum(wind_speed)/ len(wind_speed)
        data[day] = temp

    #data is aquired for all days in the date range
    #print(data)

    return data



#MAIN
if __name__ == "__main__":
    lat = 42.21
    lon = -83.36
    startDate = '2020-11-24'
    endDate = '2020-11-30'
    #do api query
    data = test_new(lat,lon,startDate,endDate)
    #plots
    plots.makePlots(data)
