#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:06:15 2022

@author: guib
"""
from netCDF4 import Dataset, num2date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import figure
# import os
import argparse

# def dir_path(string):
#     if os.path.isdir(string):
#         return string
#     else:
#         raise NotADirectoryError(string)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = min(range(len(array)), key=lambda i: abs(array[i]-value))
    return idx

def plot_var(x1,y1):
    figure(figsize=(8, 6), dpi=80)
    plt.plot(x1, y1, label=["ERA5", var], color="firebrick")
    plt.title('Wind Speed (m/s) - Perdigão')
    plt.legend(loc="lower right")
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=2))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
    plt.gcf().autofmt_xdate() # Rotation
    plt.xlim([x1.min(), x1.max()])
    
    return

def read_time(ds):
    time_var = ds.variables['time']
    dtime = num2date(time_var[:],time_var.units)
    n=len(dtime)
    x=[]
    x_datetime_global=[]

    for i in range(n):
        x.append(dtime[i].strftime('%Y-%m-%d %H:%M:%S')) # convert it to string
        x_datetime=pd.to_datetime(x) #convert it to datetime format

    x_datetime_global.append(x_datetime)
    x=np.concatenate((x_datetime_global), axis=None)
    return x

# Read ERA5 data
# input
# path = "/home/guib/Doct/Build_WRF/DATA/ERA5/perdigao/2016_2years/"
var1 = "u100"
var2 = "v100"
# #perdigão
# lon=-37.75
# lat=-4.45
var = [(var1, var2)]



parser = argparse.ArgumentParser(
    description="""
    Plot ERA5 wind speed time series \n
    format="path/file.nc"
    """
)

parser.add_argument(
    "-f", "--file", type=str, required=True,
    help="netCDF ERA5 file to plot",
)

parser.add_argument(
    "-v", "--var", default="wspd", type=str,
    help="Desired Variable",
)

parser.add_argument(
    "-lat", "--lat_ref", default=0, type=float,
    help="Central latitude.",
)

parser.add_argument(
    "-lon", "--lon_ref", default=0, type=float,
    help="Central longitude.",
)

args = parser.parse_args()
print("Input files:", args.file)

# Modify to read wspd as variable
if args.var == "wspd":
    args.var = var


nc_ERA5 = Dataset(args.file, mode='r')

lons = nc_ERA5.variables['longitude'][:]
lats = nc_ERA5.variables['latitude'][:]

lon_index=find_nearest(lons, args.lon_ref)
lat_index=find_nearest(lats, args.lat_ref)

u, v = nc_ERA5[var1], nc_ERA5[var2]

u2 = u[:,lat_index,lon_index]
v2 = v[:,lat_index,lon_index]

u3 = np.asarray(u2)
v3 = np.asarray(v2)

wspd = pow(u3*u3+v3*v3,0.5)

# X "dates" axis
x = read_time(nc_ERA5)

plot_var(x,wspd)
