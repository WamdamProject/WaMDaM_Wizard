#
#  query seasonal data:
# Input paramters: ObjectTypeCV,InstanceNameCV,AttributeNameCV
# return: df_Seasonal

import pandas as pd
from collections import OrderedDict

import csv
import os
def Seasonal_query(conn,multi_Seasonal):
    total_df_Seasonal = []
    for input_param in multi_Seasonal:
        Seasonal_query="""
        Select ScenarioName,ObjectTypeCV,ObjectType,AttributeName_Abstract,AttributeDataTypeCV,InstanceName,SeasonName,UnitName,
        SourceName,MethodName,
        SeasonNumericValue,SeasonOrder
        --,Longitude_x,Latitude_y
        
        FROM ResourceTypes
        LEFT JOIN "ObjectTypes" 
        ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID"
        
        -- Join the Objects to get their attributes  
        LEFT JOIN  "Attributes"
        ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID"
        
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
        
        LEFT JOIN "Scenarios" 
        ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID"
        
        LEFT JOIN "MasterNetworks" 
        ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID"
        
        LEFT join "Methods"
        ON "Methods"."MethodID" = "Mappings"."MethodID"
        
        LEFT join "Sources" 
        ON "Sources"."SourceID" = "Mappings"."SourceID"
        
        
        -- Join the ValuesMapper to get their Seasonal 
        LEFT JOIN "SeasonalNumericValues"
        ON "SeasonalNumericValues"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID"
        
        -- Join the ValuesMapper to get their Numeric parameters   
        LEFT JOIN "NumericValues"
        ON "NumericValues"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID"
        
        
        WHERE  
        
        
        AttributeDataTypeCV IN ('SeasonalNumericValues' ) and SeasonNumericValue is not null
    
        AND ObjectType= '%s'

        AND AttributeName_Abstract='%s'
        AND InstanceName='%s'
            AND ScenarioName='%s' 

        ORDER BY ResourceTypeAcronym,ObjectType,AttributeName_Abstract,InstanceName, ScenarioName,SeasonOrder,SeasonName ASC

     """%(input_param[1]['ObjectType'],  input_param[1]['AttributeName_Abstract'],
          input_param[1]['InstanceName'],input_param[1]['ScenarioName'] )


        df_Seasonal = pd.DataFrame(list(conn.execute(Seasonal_query)))

        df_Seasonal_columns = list(conn.execute(Seasonal_query).keys())
        df_Seasonal.columns = df_Seasonal_columns

        total_df_Seasonal.append(df_Seasonal)

    return total_df_Seasonal


def Seasonal_csv_file(total_df_Seasonal, weap_area_directory):

    # Write
    # the order is important and should follow SeasonOrder
    # csv_file_name=MonthlyValues(Oct, 2001.129097824,  Nov, 0,  Dec, 0,  Jan, 0,  Feb, 0,  Mar, 0,  Apr, 233.0187792768,  May, 6825.73055897952,  Jun, 8624.4617824848,  Jul, 8854.23757824,  Aug, 8302.97203256736,  Sep, 5680.03922474026 )
    csv_file_path_or_value_seasonal_all = []
    csv_fileName_total=[]
    Metadata_seasonal= []
    Multi_df_Seasonal=[]


    output_dir = weap_area_directory +"/Seasonal_csv_files/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)



    # SeasonName,SeasonNumericValue
    for df_Seasonal in total_df_Seasonal:
        if len(df_Seasonal['AttributeName_Abstract']) < 2: continue
        SeasonalParam = ''
        # print df_Seasonal['SeasonName']
        for i in range(len(df_Seasonal['SeasonName'])):
            m_data = df_Seasonal['SeasonName'][i]
            n_data = df_Seasonal['SeasonNumericValue'][i]
            SeasonalParam += '{},{}'.format(m_data, n_data)
            if i != len(df_Seasonal['SeasonName']) - 1:
                SeasonalParam += ','

        csv_file_path_or_value_seasonal="MonthlyValues("+SeasonalParam+")"


        x = df_Seasonal['AttributeName_Abstract'][1]
        y = df_Seasonal['InstanceName'][1]
        z = x.replace(" ", "_")
        w = y.replace(" ", "_")

        csv_fileName = output_dir + z + '_' + w + '.csv'

        Metadata_seasonal1 = OrderedDict()

        Metadata_seasonal1['Value'] =csv_file_path_or_value_seasonal
        Metadata_seasonal1['csv_fileName'] =csv_fileName

        Metadata_seasonal.append(Metadata_seasonal1)

        Multi_df_Seasonal.append(df_Seasonal)


        # print csv_file_seasonal_multi_columns

        # # save the three columns into a csv file with a name csv_file_name

        # save the the multi columns into a csv file with a name csv_file_name
        field_names = ['ObjectTypeCV', 'InstanceName', 'ScenarioName', 'AttributeName_Abstract', 'SeasonName', 'SeasonNumericValue',
                       'SeasonOrder']

        # add them into a folder called "Seasonal_Input_Files"
        f3 = open(csv_fileName, "wb")
        writer1 = csv.writer(f3, delimiter=',', quoting=csv.QUOTE_ALL)
        writer1.writerow(field_names)

        for j in range(len(df_Seasonal['SeasonNumericValue'])):
            try:
                field_values = [df_Seasonal['ObjectTypeCV'][j], df_Seasonal['InstanceName'][j],
                                df_Seasonal['ScenarioName'][j], df_Seasonal['AttributeName_Abstract'][j]
                    , df_Seasonal['SeasonName'][j], df_Seasonal['SeasonNumericValue'][j], df_Seasonal['SeasonOrder'][j]]
                writer1.writerow(field_values)
            except:
                break

        f3.close()

        # combne many output paramters here to pass them to the metadata writing file




    return Multi_df_Seasonal,Metadata_seasonal
