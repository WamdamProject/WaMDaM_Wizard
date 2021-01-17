#
#  query Time series data:
# Input paramters: ObjectTypeCV,InstanceNameCV,AttributeName_AbstractCV
# return: df_TimeSeries
import csv
from collections import OrderedDict
import xlsxwriter
import datetime, os

import pandas as pd
#
# from ..ConnectDB_ParseExcel import DB_Setup
# from ..ConnectDB_ParseExcel import SqlAlchemy as sq
# from sqlalchemy.orm import aliased

# class GetTimeSeries(object):
#     def __init__(self):
#         self.setup = DB_Setup()
#         self.session = self.setup.get_session()
#         self.excel_pointer = None

# def TimeSeries_query( session):

def TimeSeries_query(conn,multi_timeseries):
    total_df_TimeSeries =[]
    TimeSeries_Full_Branch_total = []

    for input_param in multi_timeseries:
        TimeSeries_query="""SELECT ResourceTypeAcronym,ObjectType,ScenarioName,InstanceName,AttributeName_Abstract, AggregationStatisticCV,IntervalTimeUnitCV,UnitName,SourceName,
            MethodName,PeopleSources.PersonName As SourcePerson,OrganizationsSources.OrganizationName As SoureOrganization,DateTimeStamp,DataValue
            
            FROM "ResourceTypes"
    
             Left JOIN "ObjectTypes" 
            ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID"
    
             -- Join the Objects to get their attributes  
             LEFT JOIN  "Attributes"
             ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID"
    
             LEFT JOIN "AttributeCategories" 
             ON "AttributeCategories"."AttributeCategoryID"="Attributes"."AttributeCategoryID"
    
             LEFT JOIN "Mappings"
             ON "Mappings"."AttributeID"= "Attributes"."AttributeID"
    
             LEFT JOIN "Instances" 
             ON "Instances"."InstanceID"="Mappings"."InstanceID"
    
             LEFT JOIN "InstanceCategories" 
             ON "InstanceCategories"."InstanceCategoryID"="Instances"."InstanceCategoryID"
    
             LEFT JOIN "ValuesMapper" 
             ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID"
    
             LEFT JOIN "ScenarioMappings"
             ON "ScenarioMappings"."MappingID"="Mappings"."MappingID"
    
            Left JOIN "Methods" 
            ON "Methods"."MethodID"="Mappings"."MethodID"
    
            Left JOIN "Sources" 
            ON "Sources"."SourceID"="Mappings"."SourceID"
    
            Left JOIN "People" As "PeopleSources"
            ON "PeopleSources"."PersonID"="Sources"."PersonID"
    
            Left JOIN "People" As "PeopleMethods" 
            ON "PeopleMethods"."PersonID"="Methods"."PersonID"
    
            Left JOIN "Organizations" As "OrganizationsMethods" 
            ON "OrganizationsMethods" ."OrganizationID"="PeopleMethods"."OrganizationID"
    
            Left JOIN "Organizations" As "OrganizationsSources" 
            ON "OrganizationsSources" ."OrganizationID"="PeopleSources"."OrganizationID"
    
             LEFT JOIN "Scenarios" 
             ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID"
    
             LEFT JOIN "MasterNetworks" 
             ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID"
           
            LEFT JOIN "TimeSeries" 
            ON "TimeSeries"."ValuesMapperID"="ValuesMapper"."ValuesMapperID"
            
            LEFT JOIN "TimeSeriesValues" 
            ON "TimeSeriesValues"."TimeSeriesID"="TimeSeries"."TimeSeriesID"
                
            WHERE 
            AttributeDataTypeCV='TimeSeries' and DataValue is not null
            
            AND ObjectType= '%s' 
        
            AND AttributeName_Abstract='%s'
            
            AND InstanceName='%s' 
            
            AND ScenarioName='%s' 

            
     """%(input_param[1]['ObjectType'],  input_param[1]['AttributeName_Abstract'],
          input_param[1]['InstanceName'] ,input_param[1]['ScenarioName'])

        df_TimeSeries = pd.DataFrame(list(conn.execute(TimeSeries_query)))

        df_TimeSeries_columns = list(conn.execute(TimeSeries_query).keys())
        df_TimeSeries.columns = df_TimeSeries_columns

        total_df_TimeSeries.append(df_TimeSeries)


    return total_df_TimeSeries  # pass this value into the csv function next


def Timeseries_csv_file(total_df_TimeSeries, weap_area_directory):

# Write to csv file name dynamicly:
# csv_file_name=AttributeName_Abstract_InstanceName.csv
#
# Replace any space within the AttributeName_Abstract or the the InstanceName with underscore
# AttributeName_Abstract=Headflow
# InstanceName=BlacksmithFork Inflow
#
# e.g,
# csv_file_name=Headflow_Blacksmith_Fork_Inflow.csv
#
#
# Column1, Column2, column3
# Year(YYYY),Month(MM),Value
# 1999,10,0.4
# 2000,11,0.6
    total_csv_file_name = []

    total_timeSeriesValue=[]

    Multi_df_TimeSeries = []


    Metadata_TimeSeries = []


    output_dir = weap_area_directory +"\TimeSeries_csv_files\\"

    # output_dir = "TimeSeries_csv_files\\"


    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for df_TimeSeries in total_df_TimeSeries:
        if len(df_TimeSeries['AttributeName_Abstract']) < 2: continue
        x = df_TimeSeries['AttributeName_Abstract'][1]
        # print x
        y = df_TimeSeries['InstanceName'][1]

        z = x.replace(" ", "_")

        w = y.replace(" ", "_")


        csv_file_name = output_dir + z + '_' + w + '.csv'
        # print csv_file_name
        # total_csv_file_name.append(csv_file_name)

        # there are more complex issues regarding what to do with missing values
        timeSeriesValue = "ReadFromFile(" + csv_file_name + ")"
        # total_timeSeriesValue.append(timeSeriesValue)

            # combne many output paramters here to pass them to the metadata writing file
        Metadata_TimeSeries1 = OrderedDict()

        Metadata_TimeSeries1['Value'] = timeSeriesValue

        Metadata_TimeSeries1['csv_fileName'] = csv_file_name
        # print('Writing csv file: {}'.format(csv_file_name))


        Metadata_TimeSeries.append(Metadata_TimeSeries1)

        Multi_df_TimeSeries.append(df_TimeSeries)
        x_data = df_TimeSeries['DateTimeStamp']
        # print x

        # save the three columns into a csv file with a name csv_file_name
        field_names = ['Column1', 'Column2', 'Column3']
        f1 = open(csv_file_name, "wb")

        writer = csv.writer(f1, delimiter=',', quoting=csv.QUOTE_NONE)
        # writer.writerow(field_names)

        # for ii in x:

        x = []
        # print type(x).__name__
        # print x_data[0]

        # save all of   theDemaned Sitem into a folder called: TimeSeries_csv_files

        for i in range(len(x_data)):
            year, month, date = x_data[i].split('-')
            # year.append(i)
            # month = month.append
            yx = df_TimeSeries['DataValue'][i]
            #     print year
            #     print month

            # print year, month, date
            # year,month,date=Column1.str.split('-')

            # field_names = ['Column1', 'Column2', 'column3']

            Column1 = year
            Column2 = month
            Column3 = yx

            writer.writerow([Column1, Column2, Column3])
        f1.close()
        # return csv_file_name



    return Multi_df_TimeSeries,Metadata_TimeSeries
