import os
# import numpy as np
import pandas as pd         #pip install pandas
import glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import netCDF4 as nc        #pip install netCDF4
# import matplotlib.pyplot as plt #pip install matplotlib
# import matplotlib.cm as cm
# import matplotlib.dates as d
#https://github.com/python-windrose/windrose
# from windrose import WindroseAxes #pip install windrose
# from windrose import plot_windrose
# import xarray as xr
# from scipy import stats
# import datetime as dt


########################################
#PARAMETERS                 #Name of the columns
########################################
WS78 = 'WS(2)'              #Wind Speed at 78 m
WD78 = 'WD(1)'              #Wind Direct at 78 m
# dataCPFL = data             #Dataframe name



#the files have to be inside the same folder
#print current directory
path = os.getcwd()
print("Current directory: ", path)


#read the .csv and transforming it into a dataframe
##data = pd.read_csv('Wind_487@Y2016_M04_D15.CSV', skiprows=1)

#get data file names
path =r'/home/guib/Doct/UFSC_Data/Canoa Quebrada/04-Dados_brutos-20220327T215733Z-001/04-Dados_brutos/2020-12'
print("Data directory: ", path)
filenames = sorted(glob.glob(path + "/*.wnd"))

path2 = r'/home/guib/Doct/UFSC_Data/Canoa Quebrada/04-Dados_brutos-20220327T215733Z-001/04-Dados_brutos/2020-12'

#get names of the columns 
header = pd.read_csv(path2 + '/ID880005_20201201_071848.wnd' ,delim_whitespace=True,header =2, nrows=0)

dfs = []
for filename in filenames:
    dfs.append(pd.read_csv(filename, skiprows=4, delim_whitespace=True, header=None, thousands='.', decimal=',', engine = 'python', encoding='latin-1'))

#concatenate all data into one DataFrame
dataCPFL = pd.concat(dfs, ignore_index=True)

dataCPFL.columns = header.columns

dataCPFL['DateTime'] = dataCPFL['Date'] + " " + dataCPFL['Time']

# sort values by DateTime
dataCPFL = dataCPFL.sort_values(by="DateTime")

# convert to datetime type
dataCPFL["DateTime"] = dataCPFL["DateTime"].apply(pd.to_datetime)

# converting time to GTC time zone (for future comparisons with ERA data)
dataCPFL['DateTime']=dataCPFL['DateTime']+ pd.DateOffset(hours=3)

# Velocity profile between desired dates
dataCPFL['WS(1)'] = dataCPFL['WS(1)'][(0<=dataCPFL['WS(1)'] )&(dataCPFL['WS(1)'] <=25)]
mask = (dataCPFL["DateTime"] > '2020-12-01 00:00') & (dataCPFL["DateTime"] <= '2020-12-16 00:00')
dataCPFL = dataCPFL.loc[mask]

# if hourly data is desired, run the code below
dataCPFL.index = dataCPFL["DateTime"]
dataCPFL = dataCPFL.resample('60Min', base=0, label='right').first()


# plot
plt.plot(dataCPFL["DateTime"], dataCPFL['WS(1)'])
# Ensure a major tick for each day
plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=2))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
plt.gcf().autofmt_xdate() # Rotation
plt.ylabel('Wind Speed (m/s)')
plt.title('Canoa Quebrada (December 2020)')
plt.xlim([dataCPFL["DateTime"].min(), dataCPFL["DateTime"].max()])
plt.ylim([0, 16])
plt.show()
