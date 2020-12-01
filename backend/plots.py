import numpy as np                  # mathematical operations on lists
import matplotlib.pyplot as plt     # plotting library
from io import BytesIO
import base64


    # figfile = BytesIO()
    # plt.savefig(figfile, format='png')
    # figfile.seek(0)
    # figdata_png = base64.b64encode(figfile.getvalue())
    # plot_images.append(figdata_png)
    # return plot_images
def makePlots(data):
    # datalist is: calvec, PRCP, SNOW, SNWD, TMAX, TMIN, ACSC, AWDR, AWND, TAVG
    # units:        date,   in,   in,    in,   *F,  *F,   %,    *,   mph,   *F
    plot_images = []
    dates, prcp, snow, snwd, tmax, tmin, acsc, awdr, awnd, tavg, viz, hum = ([] for i in range (12))

    for date in data.keys():
        day_data = data[date]
        dates.append(date)
        prcp.append(day_data['totalprecip_in'])
        snow.append(day_data['snow_in'])
        tmax.append(day_data['maxtemp_f'])
        tmin.append(day_data['mintemp_f'])
        acsc.append(day_data['avg_cloud_cover_percent'])
        awdr.append(day_data['avg_wind_dir'])
        awnd.append(day_data['avg_wind_speed'])
        tavg.append(day_data['avgtemp_f'])
        viz.append(day_data['avgvis_miles'])
        hum.append(day_data['avghumidity'])

    duse = dates
    xvals = range(0,7)
    # get temp limits by rounding to nearest 5 past bounds
    tn = np.min(tmin)
    tx = np.max(tmax)
    tlims = [5*(np.floor(tn/5)-1), 5*(np.ceil(tx/5)+1)]


    #need to draw boxes
    yvec45 = list(range(len(awnd)))
    for i in yvec45: yvec45[i] = 45
    yvec135 = list(range(len(awnd)))
    for i in yvec135: yvec135[i] = 135
    yvec225 = list(range(len(awnd)))
    for i in yvec225: yvec225[i] = 225
    yvec315 = list(range(len(awnd)))
    for i in yvec315: yvec315[i] = 315
    yvec360 = list(range(len(awnd)))
    for i in yvec360: yvec360[i] = 360

    fig, ((ax1,ax2)) = plt.subplots(1,2,figsize=(10, 6))
    ax1.bar(range(len(awnd)),awnd, 0.8, color='darkgray')
    ax1.set_title('Wind Speed', fontweight='bold', fontsize=24)
    ax1.set_ylabel('Miles per hour', color='black', fontweight='bold',fontsize=18)
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_xlabel('Date', fontweight='bold',fontsize=18)
    ax1.set_xticks(ticks=xvals)
    ax1.set_xticklabels(labels=duse,rotation=45)

    ax2.plot(range(len(awdr)),awdr, color='black', linewidth=2, marker='o', markersize=6)
    ax2.set_title('Wind Direction', fontweight='bold', fontsize=24)
    ax2.set_ylim(0,360)
    ax2.set_yticks(ticks=range(0,360,45))
    ax2.set_ylabel('Degrees E of N',color='black', fontweight='bold',fontsize=18)
    ax2.tick_params(axis='y', labelcolor='black')
    ax2.yaxis.set_label_position("right")
    ax2.yaxis.tick_right()
    ax2.bar(xvals,yvec360,1.0,color='lightsteelblue')
    ax2.bar(xvals,yvec315,1.0,color='papayawhip')
    ax2.bar(xvals,yvec225,1.0,color='salmon')
    ax2.bar(xvals,yvec135,1.0,color='lightgreen')
    ax2.bar(xvals,yvec45,1.0,color='lightsteelblue')
    curxlim = ax1.get_xlim()
    ax2.text(-0.5, 10, 'N', color='midnightblue', fontweight='bold', fontsize=24)
    ax2.hlines(45,curxlim[0],curxlim[1],color='lightgray',linestyle='--')
    ax2.text(-0.5, 80, 'E', color='olivedrab', fontweight='bold', fontsize=24)
    ax2.hlines(135,curxlim[0],curxlim[1],color='lightgray',linestyle='--')
    ax2.text(-0.5, 170, 'S', color='red', fontweight='bold', fontsize=24)
    ax2.hlines(225,curxlim[0],curxlim[1],color='lightgray',linestyle='--')
    ax2.text(-0.5, 260, 'W', color='peru', fontweight='bold', fontsize=24)
    ax2.hlines(315,curxlim[0],curxlim[1],color='lightgray',linestyle='--')
    ax2.text(-0.5, 325, 'N', color='midnightblue', fontweight='bold', fontsize=24)
    ax2.set_xlabel('Date', fontweight='bold',fontsize=18)
    ax2.set_xticks(ticks=xvals)
    ax2.set_xticklabels(labels=duse,rotation=45)

    plt.tight_layout()
   # plt.savefig('testWIND.jpg')
    # plt.show()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    plot_images.append(figdata_png)



    # xvals for side dashes
    xsides = list(range(len(tavg)+1))
    for i in xsides: xsides[i] = xsides[i] - 0.5

    # plot for temp+precipR/S
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(range(len(tavg)),tavg, color='red', linewidth=2, marker='o', markersize=6)
    if tlims[0] < 32:
        curxlim = ax1.get_xlim()
        ax1.hlines(32,curxlim[0]-0.5,curxlim[1]+0.5,color='lightcoral',linestyle='--')
        ax1.text(-0.8, 33, '32*F', color='lightcoral', fontsize=14, rotation=90)
    ax1.set_ylim(tlims)
    curylim = ax1.get_ylim()
    ax1.vlines(xsides,curylim[0],curylim[1],color='silver',linestyle='--')
    ax1.set_xlabel('Date', fontweight='bold',fontsize=18)
    ax1.set_ylabel('Average Temperature (*F)',color='red', fontweight='bold',fontsize=18)
    ax1.tick_params(axis='y', labelcolor='red')
    plt.xticks(ticks=xvals, labels=duse)
    plt.xticks(rotation=0)

    width = 0.35/2
    xbarm = list(range(len(snow)))
    for ii in range(len(xbarm)): xbarm[ii] = xbarm[ii] - width
    xbarp = list(range(len(snow)))
    for ii in range(len(xbarp)): xbarp[ii] = xbarp[ii] + width


    ax2 = ax1.twinx()
    ax2.bar(xbarm,snow, width*1.75, color='blue')
    ax2.bar(xbarp,prcp, width*1.75, color='green')
    ax2.set_ylabel('Precipitation (in)', color='black', fontweight='bold',fontsize=18)
    ax2.tick_params(axis='y', labelcolor='black')
    ax1.plot(range(len(tavg)),tavg, color='red', linewidth=2, marker='o', markersize=6)
    curxlim = ax2.get_xlim()
    curylim = ax2.get_ylim()
    xtxt = curxlim[1]-0.2*(curxlim[1]-curxlim[0])
    lin1 = curylim[1]-0.1*(curylim[1]-curylim[0])
    lin2 = curylim[1]-0.15*(curylim[1]-curylim[0])
    plt.text(xtxt,lin1,'Rain',color='green',fontweight='bold',fontsize=18)
    plt.text(xtxt,lin2,'Snow',color='blue',fontweight='bold',fontsize=18)
    plt.title('Temperature and Precipitation',  fontweight='bold', fontsize=24)
    plt.tight_layout()
   # plt.savefig('testTP.jpg')
    # plt.show()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    plot_images.append(figdata_png)



    # plot for temp min/max/avg
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.fill_between(range(len(tmin)),tmin,tmax, color='mediumseagreen')
    ax1.plot(range(len(tmin)),tmin, color='blue', linewidth=2,marker='o', markersize=6)
    ax1.plot(range(len(tavg)),tavg, color='darkgreen',linewidth=2,marker='o', markersize=6)
    ax1.plot(range(len(tmax)),tmax, color='red',linewidth=2,marker='o', markersize=6)
    ax1.set_ylim(tlims)
    curylim = ax1.get_ylim()
    curxlim = ax1.get_xlim()
    xtxt1 = curxlim[1]-0.3*(curxlim[1]-curxlim[0])
    xtxt2 = curxlim[1]-0.5*(curxlim[1]-curxlim[0])
    xtxt3 = curxlim[1]-0.7*(curxlim[1]-curxlim[0])
    xtxt4 = curxlim[1]-0.9*(curxlim[1]-curxlim[0])
    lin1 = curylim[1]-0.08*(curylim[1]-curylim[0])
    ax1.text(xtxt1,lin1,'MAX',color='red',fontweight='bold',fontsize=18)
    ax1.text(xtxt2,lin1,'AVG',color='darkgreen',fontweight='bold',fontsize=18)
    ax1.text(xtxt3,lin1,'SPREAD',color='white',fontweight='bold',fontsize=18,
        bbox=dict(boxstyle="square",ec='mediumseagreen',fc='mediumseagreen'))
    ax1.text(xtxt4,lin1,'MIN',color='blue',fontweight='bold',fontsize=18)
    if tlims[0] < 32:
        ax1.hlines(32,curxlim[0]-0.5,curxlim[1]+0.5,color='silver',linestyle='--')
        ax1.text(-0.8, 30, '32*F', color='silver', fontsize=14, rotation=0)
    ax1.set_ylim(tlims)
    curylim = ax1.get_ylim()
    ax1.vlines(xvals,curylim[0],curylim[1],color='silver',linestyle='--')
    ax1.set_xlabel('Date', fontweight='bold',fontsize=18)
    ax1.set_ylabel('Temperature (*F)',color='black', fontweight='bold',fontsize=18)
    ax1.tick_params(axis='y', labelcolor='black')
    plt.xticks(ticks=xvals, labels=duse)
    plt.xticks(rotation=0)

    plt.title('Temperature',  fontweight='bold', fontsize=24)
    plt.tight_layout()
   # plt.savefig('test3TEMP.jpg')
    # plt.show()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    plot_images.append(figdata_png)

    # plot for %cloudy viz, hum
    fig, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(range(len(viz)),viz, 0.75,color='lightskyblue')
    curylim = ax2.get_ylim()
    ax2.set_ylim([curylim[0], curylim[1]*1.1])
    ax2.set_ylabel('Visibility (mi)', color='blue', fontweight='bold',fontsize=18)
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.set_xlabel('Date', fontweight='bold',fontsize=18)
    plt.title('Visibility, Humidity, and Cloudiness',  fontweight='bold', fontsize=24)


    ax1 = ax2.twinx()
    ax1.plot(range(len(acsc)),acsc, color='blue', linewidth=2, marker='o', markersize=6)
    ax1.plot(range(len(hum)),hum, color='red', linewidth=2, marker='o', markersize=6)
    ax1.set_ylim([0,110])
    curylim = ax1.get_ylim()
    lin1 = curylim[1]-0.05*(curylim[1]-curylim[0])
    curxlim = ax1.get_xlim()
    xtxt1 = curxlim[1]-0.35*(curxlim[1]-curxlim[0])
    xtxt2 = curxlim[1]-0.15*(curxlim[1]-curxlim[0])
    ax1.hlines(50,curxlim[0],curxlim[1],color='silver',linestyle='--')
    ax1.text(6.5, 52, '50%', color='silver', fontsize=14, rotation=0)
    ax1.text(xtxt1,lin1,'Humidity',color='red',fontweight='bold',fontsize=18)
    ax1.text(xtxt2,lin1,'Cloudiness',color='blue',fontweight='bold',fontsize=18)
    ax1.set_xlabel('Date', fontweight='bold',fontsize=18)
    ax1.set_ylabel('Percent (%)',color='black',fontweight='bold',fontsize=18)
    plt.xticks(ticks=xvals, labels=duse)
    plt.xticks(rotation=0)

    plt.tight_layout()
    # plt.savefig('testVCH.jpg')
    # plt.show()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    plot_images.append(figdata_png)

    return plot_images
