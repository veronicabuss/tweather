# import requests                     # needed to make web requests
# import pandas as pd                 # store the data we get as a dataframe
# import json                         # convert the response as a strcuctured json
import numpy as np                  # mathematical operations on lists
# from datetime import datetime       # parse the datetimes we get from NOAA
import matplotlib.pyplot as plt     # plotting library
# import math                         # math functions
# import os                           # os functions
# import csv                          # csv file funcitons

def makePlots(sta,data):
    # datalist is: calvec, PRCP, SNOW, SNWD, TMAX, TMIN, ACSC, AWDR, AWND, TAVG, WV03
    # units:        date,   in,   in,    in,   *F,  *F,   %,    *,   mph,   *F,   #
    # breakout datalist
    staname = sta[1][2]
    dates = data[0]; prcp = data[1]; snow = data[2]; snwd = data[3]
    tmax = data[4]; tmin = data[5]; acsc = data[6]; awdr = data[7]
    awnd = data[8]; tavg = data[9]; wv03 = data[10]

    nobs = len(dates)
    doobs = np.floor(nobs/10)

    duse = []
    xvals = []
    ii = 0
    while ii < nobs:
        xvals.append(ii)
        duse.append(dates[ii])
        ii = int(ii + np.floor(nobs/10))

    # plot for wind speed+direction

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(range(len(awdr)),awdr, color='blue', linewidth=2, marker='o', markersize=6)
    curylim = ax1.get_ylim()
    ax1.vlines(xvals,curylim[0],curylim[1],color='silver',linestyle='--')
    ax1.set_xlabel('Date', fontweight='bold')
    ax1.set_ylabel('Wind Direction (deg E of N)',color='blue', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='blue')
    plt.xticks(ticks=xvals, labels=duse)
    plt.xticks(rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(range(len(awnd)),awnd, color='red', linewidth=2, marker='o', markersize=6)
    ax2.set_ylabel('Wind Speed (MPH)', color='red', fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='red')
    plt.title('Winds',  fontweight='bold', fontsize=24)
    plt.tight_layout()
   # plt.savefig('testWIND.jpg')
    plt.show()


    # plot for temp+precipR/S
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(range(len(tavg)),tavg, color='red', linewidth=2, marker='o', markersize=6)
    curxlim = ax1.get_xlim()
    ax1.hlines(32,curxlim[0],curxlim[1],color='lightcoral',linestyle='--')
    curylim = ax1.get_ylim()
    ax1.vlines(xvals,curylim[0],curylim[1],color='silver',linestyle='--')
    ax1.set_xlabel('Date', fontweight='bold')
    ax1.set_ylabel('Average Temperature (*F)',color='red', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='red')
    plt.xticks(ticks=xvals, labels=duse)
    plt.xticks(rotation=45)

    width = 0.35
    xbar = list(range(len(snow)))
    for ii in range(len(xbar)): xbar[ii] = xbar[ii] + width

    ax2 = ax1.twinx()
    ax2.bar(range(len(snow)),snow, width, color='blue')
    ax2.bar(xbar,prcp, width, color='green')
    ax2.set_ylabel('Precipitation (in)', color='black', fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='black')
    curxlim = ax2.get_xlim()
    curylim = ax2.get_ylim()
    xtxt = curxlim[1]-0.2*(curxlim[1]-curxlim[0])
    lin1 = curylim[1]-0.1*(curylim[1]-curylim[0])
    lin2 = curylim[1]-0.15*(curylim[1]-curylim[0])
    plt.text(xtxt,lin1,'Rain',color='green',fontweight='bold')
    plt.text(xtxt,lin2,'Snow',color='blue',fontweight='bold')
    plt.title('Temperature and Precipitation',  fontweight='bold', fontsize=24)
    plt.tight_layout()
   # plt.savefig('testTP.jpg')

    plt.show()


    # plot for temp min/max/avg
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.fill_between(range(len(tmin)),tmin,tmax, color='mediumseagreen')
   # ax1.plot(range(len(tmin)),tmin, color='blue', linewidth=2)
    ax1.plot(range(len(tavg)),tavg, color='darkgreen', linewidth=2)
   # ax1.plot(range(len(tmax)),tmax, color='red', linewidth=2)
    curxlim = ax1.get_xlim()
    ax1.hlines(32,curxlim[0],curxlim[1],color='silver',linestyle='--')
    curylim = ax1.get_ylim()
    ax1.vlines(xvals,curylim[0],curylim[1],color='silver',linestyle='--')
    ax1.set_xlabel('Date', fontweight='bold')
    ax1.set_ylabel('Temperature (*F)',color='black', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='black')
    plt.xticks(ticks=xvals, labels=duse)
    plt.xticks(rotation=45)

    plt.title('Temperature',  fontweight='bold', fontsize=24)
    plt.tight_layout()
   # plt.savefig('test3TEMP.jpg')
    plt.show()

    # plot for %-cloudy and Tstorm
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(range(len(acsc)),acsc, color='blue', linewidth=2, marker='o', markersize=6)
    curylim = ax1.get_ylim()
    ax1.vlines(xvals,curylim[0],curylim[1],color='silver',linestyle='--')
    curxlim = ax1.get_xlim()
    ax1.hlines(50,curxlim[0],curxlim[1],color='silver',linestyle='--')
    ax1.set_xlabel('Date', fontweight='bold')
    ax1.set_ylabel('%-cloudy',color='blue', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='blue')
    plt.xticks(ticks=xvals, labels=duse)
    plt.xticks(rotation=45)


    ax2 = ax1.twinx()
    ax2.plot(range(len(snwd)),snwd, color='red', linewidth=2, marker='o', markersize=6)
    ax2.set_ylabel('Snow Depth (in)', color='red', fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='red')
    plt.title('%-cloudy and Snow Depth',  fontweight='bold', fontsize=24)
    plt.tight_layout()
   # plt.savefig('testSD.jpg')
    plt.show()


    # plot for histograms
    tempbins = [-20,-15,-10,-5,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]
    fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(3,2,figsize=(10, 6))
    ax1.hist(tmax,tempbins,histtype='stepfilled',color='red')
    curylim = ax1.get_ylim(); ax1.vlines(32,curylim[0],curylim[1],color='silver',linestyle='--')
    ax3.hist(tavg,tempbins,histtype='stepfilled',color='darkgreen')
    curylim = ax3.get_ylim(); ax3.vlines(32,curylim[0],curylim[1],color='silver',linestyle='--')
    ax5.hist(tmin,tempbins,histtype='stepfilled',color='blue')
    curylim = ax5.get_ylim(); ax5.vlines(32,curylim[0],curylim[1],color='silver',linestyle='--')

    prcp[:] = [0.001 if x < 0.001 else x for x in prcp]
    snow[:] = [0.001 if x < 0.001 else x for x in snow]

    ax2.hist(np.log(prcp)/np.log(10),23,histtype='stepfilled',color='green')
    ax4.hist(np.log(snow)/np.log(10),23,histtype='stepfilled',color='blue')
    ax6.hist(awnd,23,histtype='stepfilled',color='red')


   # plt.savefig('testHIST.jpg')
    plt.show()
