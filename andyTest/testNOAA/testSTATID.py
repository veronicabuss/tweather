# this tests calculating/finding nearest station to a lon/lat
# 1) check if LOCUSE is within 4 boxes
# 2) calc great circle distances
# 3) find min dist, return station ID

import csv
import math
import numpy as np

# note: lat<0 = s.hemi; lon<0 = w.hemi

kzoo = [42.23,-85.55]
fbanks = [64.8,-147.8]
hlulu = [21.32,-157.92]
sjuan = [18.43,-66]
barca = [41.37,2.17]
melb = [-37.84,144.97]

LOCUSE = fbanks
# ^ LOCUSE always assumed [lat,lon]


#** function will need to start here with LOCUSE as input
# MATLAB-like f'n:  [staID, sLat, sLon, errmsg] = pickStation(LOCUSE)



# conus, alska, hawai, prico are [latN,latS,lonE,lonW] bounds on box for inclusion
conus = [50,24,-65,-125]
alska = [71.5,51,-128,-179]
hawai = [22.5,18.5,-154,-161]
prico = [18.5,17.5,-65,-68]

errmsg = ['PASSED box']
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

if cF+aF+hF+pF == 0: errmsg = ['FAILED box']

if errmsg[0:5] != 'PASSED':
    print('**** return to calling f''n, LAT/LON box error')

print('madeit - calc great circ')
# import station list
fname = 'isd-history-states-nohead-testing.csv'
fid = open(fname,newline='')
stations = csv.reader(fid)

radE = 3958.8   # earth radius in mi
j = 0
alldist = []
allsta = []
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
print(idx)
print(alldist[idx])
print(allsta[idx])


# add error msg if station to use is >100mi from LOCUSE
if idx > 100: errmsg.append('STATION > 100mi')

print(errmsg)
#