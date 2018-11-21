import plotly
plotly.__version__
import plotly.offline as offline
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
offline.init_notebook_mode(connected=True)
from plotly.offline import init_notebook_mode, iplot
from plotly.graph_objs import *

init_notebook_mode(connected=True)         # initiate notebook for offline plot

import pandas as pd
import os
import csv
from collections import OrderedDict
import sqlite3
import pandas as pd
import numpy as np
from IPython.display import display, Image, SVG, Math, YouTubeVideo
import urllib

print 'imported'

# Then we can run queries against it within this notebook :)

# the SQLite file is published here
#https://github.com/WamdamProject/WaMDaM_UseCases/blob/master/UseCases_files/3SQLite_database/BearRiverDatasets_June_2018.sqlite

conn = sqlite3.connect('BearRiverDatasets_June_2018.sqlite')

print 'connected'

# Use Case 3.1Identify_aggregate_TimeSeriesValues.csv
# plot aggregated to monthly and converted to acre-feet time series data of multiple sources



# 2.2Identify_aggregate_TimeSeriesValues.csv
Query_UseCase3_1_URL="""
https://raw.githubusercontent.com/WamdamProject/WaMDaM_UseCases/master/UseCases_files/4Queries_SQL/UseCase3/UseCase3.1/2_Identify_aggregate_TimeSeriesValues.sql

"""

# Read the query text inside the URL
Query_UseCase3_1_text = urllib.urlopen(Query_UseCase3_1_URL).read()


# return query result in a pandas data frame
result_df_UseCase3_1= pd.read_sql_query(Query_UseCase3_1_text, conn)

# uncomment the below line to see the list of attributes
# display (result_df_required)


# Save the datafrom as a csv file into the Jupyter notebook working space
# result_df_UseCase3_1.to_csv('UseCases_Results_csv\UseCase3_1.csv', index = False)

# Select the UDWR subset
df_TimeSeries=result_df_UseCase3_1
# identify the data for four time series only based on the DatasetAcronym column header
column_name = "ResourceTypeAcronym"
subsets = df_TimeSeries.groupby(column_name)


for subset in subsets.groups.keys():
    # print subset
    dt = subsets.get_group(name='UDWRFlowData')

# uncoment this line below if you want to see the table
# display (dt)


Metadata_TimeSeries = []

# dataframe output of WaMDaM query
df_TimeSeries = dt

# x = df_TimeSeries['AttributeName'][1]


# display(dt)

AttributeName = 'Streamflow Data'

InstanceName = 'USGS 10046500'
# print x
# y = df_TimeSeries['InstanceName'][1]


z = AttributeName.replace(" ", "_")

w = InstanceName.replace(" ", "_")

output_dir = "TimeSeries_csv_files\\"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# WEAP_Area_dir is where the WEAP Area folder exists on your machine
csv_file_name = output_dir + z + '_' + w + '.csv'
print csv_file_name
# total_csv_file_name.append(csv_file_name)

# there are more complex issues regarding what to do with missing values
timeSeriesValue = "ReadFromFile(" + csv_file_name + ")"
print timeSeriesValue
# total_timeSeriesValue.append(timeSeriesValue)

# combne many output paramters here to pass them to the metadata writing file
Metadata_TimeSeries1 = OrderedDict()

Metadata_TimeSeries1['Value'] = timeSeriesValue

Metadata_TimeSeries1['csv_fileName'] = csv_file_name

print csv_file_name
# for TimeSeries_Full_Branch in TimeSeries_Full_Branch_total:

# Metadata_TimeSeries1['FullBranch'] = TimeSeries_Full_Branch

Metadata_TimeSeries.append(Metadata_TimeSeries1)

x_data = df_TimeSeries['CalenderYear']
# print x_data

# save the three columns into a csv file with a name csv_file_name

#################################################################################
# How to save the file in the WEAP area?

field_names = ['Column1', 'Column2', 'Column3']
f1 = open(csv_file_name, "wb")

# writer = csv.writer(f1, delimiter=',', quoting=csv.QUOTE_ALL)
# writer.writerow(field_names)

# for ii in x:

x = []
# print type(x).__name__
# print x_data[0]

# save all of   them into a folder called: TimeSeries_csv_files

#############################################################
# Convert the Acre-feet per month to cfs as required by WEAP
# CumulativeMonthly


# for i in range(len(x_data)):
for i, val in x_data.iteritems():

    year, month, day = val.split('-')


    yx = df_TimeSeries['CumulativeMonthly'][i]
    # print year
    # print month

    # print year, month, date
    # year,month,date=Column1.str.split('-')

    # field_names = ['Column1', 'Column2', 'column3']

    Column1 = year
    Column2 = month
    Column3 = yx

    f1.write("{},{},{}".format(Column1, Column2, Column3))


f1.close()
# return csv_file_name