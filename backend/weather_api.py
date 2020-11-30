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


if __name__ == "__main__":
    print("This module should not be run directly")
    return

#*****  MAKE NEEDED FUNCTION DEFS
def convert_c_to_f(temp):           # convert temperature *C to *F
    tout = float(temp)/10.0*1.8 + 32
    tout = np.floor(tout*100)/100
    return tout

def convert_tenmm_to_in(precip):
    pout = float(precip)/(2.54*100)
    pout = np.floor(pout*100)/100
    return pout

def convert_mm_to_in(precip):
    pout = float(precip)/(2.54*10)
    pout = np.floor(pout*100)/100
    return pout

def convert_ms_to_mph(wspd):        # convert windspeed 1/10s m/s to mi/hr
    wout = float(wspd)/10 * 2.2369
    wout = np.floor(wout*100)/100
    return wout

# MAIN API CALL
def callNOAA(staid,beg,end):        # make api call to data from NOAA
    dataid = 'GHCND'        # daily summaries dataset

    # datasets to get: PRCP, SNOW, SNWD, TMAX, TMIN, ACSC, AWDR, AWND, TAVG, WV03
    dataIDa='&datatypeid=PRCP&datatypeid=SNOW&datatypeid=SNWD&datatypeid=TMAX&datatypeid=TMIN'
    dataIDb='&datatypeid=ACSC&datatypeid=AWDR&datatypeid=AWND&datatypeid=TAVG&datatypeid=WV03'
    typeid = dataIDa+dataIDb

    # add the access token you got from NOAA
    token = Token.token()

    # run the request
    r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid='+dataid+typeid+'&limit=1000&stationid='+staid+'&startdate='+beg+'&enddate='+end, headers={'token':token})

    # load the api response as a json
    d = json.loads(r.text)

    # write json to file if needed
    # ts = datetime.now()
    # ts = math.floor(ts.timestamp()*1000)  # store timestamp out to millisec
    # fname = staid+'_'+beg+'_'+end+'_'+str(ts)
    # fname = fname[6:]       # strip beginning 'GHCND:'
    # # wirte file for future revisit
    # curdir = os.curdir+'/weatherstore/'
    # with open(curdir+fname+'.json', 'w') as outfile: json.dump(d,outfile)
    return d        # return NOAA data as JSON object



def getData(data):          # get data vectors
    # datasets to get: PRCP, SNOW, SNWD, TMAX, TMIN, ACSC, AWDR, AWND, TAVG, WV03

    res = data['results']
    begd = (res[0]['date'][0:4],res[0]['date'][5:7],res[0]['date'][8:10])
    endd = (res[-1]['date'][0:4],res[-1]['date'][5:7],res[-1]['date'][8:10])

    calvec = bldcal(begd,endd)
    # output is a list ['YYYY-MM-01','YYYY-MM-02'..]

    #decalre data lists as missing with len(calvec)
    prcp = np.empty((1,len(calvec))); prcp.fill(np.nan); prcp = prcp[0].tolist()
    snow = np.empty((1,len(calvec))); snow.fill(np.nan); snow = snow[0].tolist()
    snwd = np.empty((1,len(calvec))); snwd.fill(np.nan); snwd = snwd[0].tolist()
    tmax = np.empty((1,len(calvec))); tmax.fill(np.nan); tmax = tmax[0].tolist()
    tmin = np.empty((1,len(calvec))); tmin.fill(np.nan); tmin = tmin[0].tolist()
    acsc = np.empty((1,len(calvec))); acsc.fill(np.nan); acsc = acsc[0].tolist()
    awdr = np.empty((1,len(calvec))); awdr.fill(np.nan); awdr = awdr[0].tolist()
    awnd = np.empty((1,len(calvec))); awnd.fill(np.nan); awnd = awnd[0].tolist()
    tavg = np.empty((1,len(calvec))); tavg.fill(np.nan); tavg = tavg[0].tolist()
    wv03 = np.empty((1,len(calvec))); wv03.fill(np.nan); wv03 = wv03[0].tolist()

    # fill data appropriately
    for ient in range(len(res)):
        for ida in range(len(calvec)):
            if calvec[ida] == res[ient]['date'][0:10]:
                if res[ient]['datatype'] == 'PRCP': prcp[ida] = convert_tenmm_to_in(res[ient]['value'])
                if res[ient]['datatype'] == 'SNOW': snow[ida] = convert_mm_to_in(res[ient]['value'])
                if res[ient]['datatype'] == 'SNWD': snwd[ida] = convert_mm_to_in(res[ient]['value'])
                if res[ient]['datatype'] == 'TMAX': tmax[ida] = convert_c_to_f(res[ient]['value'])
                if res[ient]['datatype'] == 'TMIN': tmin[ida] = convert_c_to_f(res[ient]['value'])
                if res[ient]['datatype'] == 'ACSC': acsc[ida] = res[ient]['value']
                if res[ient]['datatype'] == 'AWDR': awdr[ida] = res[ient]['value']
                if res[ient]['datatype'] == 'AWND': awnd[ida] = convert_ms_to_mph(res[ient]['value'])
                if res[ient]['datatype'] == 'TAVG': tavg[ida] = convert_c_to_f(res[ient]['value'])
                if res[ient]['datatype'] == 'WV03': wv03[ida] = res[ient]['value']

    dataout = [calvec,prcp,snow,snwd,tmax,tmin,acsc,awdr,awnd,tavg,wv03]
    return dataout




#Convert lat/lon to station id
def getStaID(LOCUSE):               # get station data from listing
    # note: LOCUSE input accepted as [lat,lon] for station
    # note: lat<0 = s.hemi; lon<0 = w.hemi
    staidout = (-9,)    # default to -9 as error, non-error is (dist2sta,sta)

    conus = [50,24,-65,-125]            # |
    alska = [71.5,51,-128,-179]         # | [latN,latS,lonE,lonW] bounds
    hawai = [22.5,18.5,-154,-161]       # | on box for inclusion
    prico = [18.5,17.5,-65,-68]         # |

    for i in range(4):
        if i == 0:
            cF = 1  # flags for boxes, 1 = LOCUSE within box
            if (LOCUSE[0] > conus[0]) or (LOCUSE[0] < conus[1]): cF = 0
            if (LOCUSE[1] > conus[2]) or (LOCUSE[1] < conus[3]): cF = 0

        if i == 1:
            aF = 1  # flags for boxes, 1 = LOCUSE within box
            if (LOCUSE[0] > alska[0]) or (LOCUSE[0] < alska[1]): aF = 0
            if (LOCUSE[1] > alska[2]) or (LOCUSE[1] < alska[3]): aF = 0

        if i == 2:
            hF = 1  # flags for boxes, 1 = LOCUSE within box
            if (LOCUSE[0] > hawai[0]) or (LOCUSE[0] < hawai[1]): hF = 0
            if (LOCUSE[1] > hawai[2]) or (LOCUSE[1] < hawai[3]): hF = 0

        if i == 3:
            pF = 1  # flags for boxes, 1 = LOCUSE within box
            if (LOCUSE[0] > prico[0]) or (LOCUSE[0] < prico[1]): pF = 0
            if (LOCUSE[1] > prico[2]) or (LOCUSE[1] < prico[3]): pF = 0

    if cF+aF+hF+pF == 0: return staidout

    # LOCUSE is within 4 US domains, find station
    # import station list
    fname = 'isd-stations-use.csv'
    fid = open(fname,newline='')
    stations = csv.reader(fid)

    radE = 3958.8   # earth radius in mi
    alldist = []; allsta = []

    for row in stations:
        allsta.append(row)
        curLAT = float(row[6])
        curLON = float(row[7])
        # great circle (Haversine) formula
        # https://en.wikipedia.org/wiki/Haversine_formula

        havLAT = (1-math.cos(math.radians(curLAT-LOCUSE[0])))/2
        havLON = (1-math.cos(math.radians(curLON-LOCUSE[1])))/2
        prodLAT = math.cos(math.radians(curLAT))*math.cos(math.radians(LOCUSE[0]))

        dist = 2*radE*math.asin(math.sqrt(havLAT+prodLAT*havLON))
        alldist.append(dist)

    idx = np.argmin(alldist)
    idxuse = idx
    if allsta[idxuse][1] == str(99999):       # if station is 99999, serch first non
        distsort = np.argsort(alldist)
        for ista in range(len(alldist)):
            if allsta[distsort[ista]][1] != str(99999):
                idxuse = distsort[ista]
                break

    staidout = (alldist[idxuse],allsta[idxuse])
    # output tuple of (dist2sta,sta-data)
    return staidout

# # MAIN API CALL
# def api_call(startDate,endDate,station_id,Token):
#     dates_temp = []
#     dates_prcp = []
#     temps = []
#     prcp = []
#
#     #make the api call
#     r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TAVG&limit=1000&stationid='+station_id+'&startdate='+startDate+'&enddate='+endDate, headers={'token':Token})
#     #load the api response as a json
#     d = json.loads(r.text)
#
#     # get all items in the response which are average temperature readings
#     avg_temps = [item for item in d['results'] if item['datatype']=='TAVG']
#     #get the date field from all average temperature readings
#     dates_temp += [item['date'] for item in avg_temps]
#     #get the actual average temperature from all average temperature readings
#     temps += [item['value'] for item in avg_temps]
#
#     #initialize dataframe
#     df_temp = pd.DataFrame()
#
#     #populate date and average temperature fields (cast string date to datetime and convert temperature from tenths of Celsius to Fahrenheit)
#     df_temp['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_temp]
#     df_temp['avgTemp'] = [float(v)/10.0*1.8 + 32 for v in temps]
#
#     print(df_temp)
#
#     return
