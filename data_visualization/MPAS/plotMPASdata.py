#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: guib
"""


from netCDF4 import Dataset, num2date
# import netCDF4 as nc
# import xarray as xr
import numpy as np
import pandas as pd
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.dates as mdates
import os
import glob
import argparse

def plot_var(x1,y1):
    figure(figsize=(8, 6), dpi=80)
    time=ds
    # plt.xlabel("Date-Hour")
    # plt.ylabel("Wind Speed (ms-1)")
    # year = x1.year[0]
    # month = x1.month[0]
    plt.title('Wind Speed (%s)(X m)' %(var))
    plt.plot(x1, y1, label=[var], color="green")
    # plt.plot(x1, y2, label=["Domain 2 (nest)"], color="orange")

    # edit the x axis (repeated below)
    # plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=2))
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
    # plt.gcf().autofmt_xdate() # Rotation
    # plt.xlim([x1.min(), x1.max()])
    # plt.ylim([290, 305])
    plt.legend(loc="lower right")
    
    
    # sns.set_style('darkgrid') # darkgrid, white grid, dark, white and ticks
    # plt.rc('axes', titlesize=18)     # fontsize of the axes title
    # plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
    # plt.rc('xtick', labelsize=13)    # fontsize of the tick labels
    # plt.rc('ytick', labelsize=13)    # fontsize of the tick labels
    # plt.rc('legend', fontsize=13)    # legend fontsize
    # plt.rc('font', size=13)          # controls default text sizes


    plt.show()

    return

def plot_var_pandas(df,var):
    
    df.plot(y='Wind Speed (m/s)', figsize=(8,6))
    plt.title('Wind Speed (%s)' %(var))
    plt.legend(loc="lower right")
    plt.show()
    
    return


# input
# path='/home/guib/Doct/MPAS/perdigao_feb/'

# path='/home/guib/Doct/MPAS/perdigao_2017_2months_9km/'

path='/home/guib/Doct/Results/MPAS/perdigao_2017_04_9km_1hour/'

var1="uReconstructMeridional"
var2="uReconstructZonal"
var=[(var1, var2)]


os.chdir(path)
filenames = sorted(glob.glob("history.*.nc"))
n=len(filenames)
u_merid = np.empty((n))
u_merid[:] = np.nan
u_zonal = np.empty((n))
u_zonal[:] = np.nan

time= []
x_time=[]


for i, filename in enumerate(filenames):
    ds=Dataset(os.path.join(path, filename), mode='r')

    
    aux=ds["uReconstructMeridional"]
    aux2=ds["uReconstructZonal"]
    u_merid[i]=float(aux[0,629,1]) #change to match Aracati data #shape(Time, nCells, nVertLevels)
    u_zonal[i]=float(aux2[0,629,1]) #change to match Aracati data
    
    time.append(filename[-22:-3])
    x_time.append(datetime.strptime(time[i], '%Y-%m-%d_%H.%M.%S'))


# ds=Dataset(os.path.join(path, filename), mode='r')
wspd=pow((u_merid*u_merid+u_zonal*u_zonal),0.5)



run_duration=ds.__dict__['config_run_duration']
start_time=ds.__dict__['config_start_time']


u2 = np.concatenate((u_merid), axis=None)
v2 = np.concatenate((u_zonal), axis=None)
# x=[]
x=np.concatenate((x_time), axis=None)

wspd = np.concatenate((wspd), axis=None)


d={'Wind Speed (m/s)':wspd,'u':u2, 'v':v2}
df_MPAS=pd.DataFrame(d,index=x)

# x=range(n)

# plot_var(x,wspd)

plot_var_pandas(df_MPAS, var)
