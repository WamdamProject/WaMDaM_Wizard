
#
# query Multi Attributes data:
# Input paramters: ObjectTypeCV,InstanceNameCV,AttributeNameCV
# return: df_MultiAttributes

import pandas as pd
import csv
import datetime
from collections import OrderedDict
import os

def MultiAttributes_query(conn,multi_AttributeSeries):
    total_df_MultiColumns = []
    Multi_Full_Branch_total = []

    for input_param in multi_AttributeSeries:
        MultiAttributes_query="""
       SELECT "ObjectTypes"."ObjectType",
        "Instances"."InstanceName",ScenarioName,"Attributes"."AttributeName" AS MultiAttributeName,
        Attributes.UnitName As UnitName,Methods.MethodName,Sources.SourceName,
        "Attributes".AttributeDataTypeCV,
        "AttributesColumns"."AttributeName" AS "AttributeName",
        "AttributesColumns"."AttributeNameCV",
        "AttributesColumns"."UnitNameCV" AS "AttributeNameUnitName",
        "DataValue","ValueOrder"
        
        FROM "ResourceTypes"
        
        -- Join the ResourceType to get its Object Types 
        LEFT JOIN "ObjectTypes" 
        ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID"
        
        -- Join the Object types to get their attributes  
        LEFT JOIN  "Attributes"
        ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID"
        
        -- Join the Attributes to get their Mappings   
        LEFT JOIN "Mappings"
        ON Mappings.AttributeID= Attributes.AttributeID
        
        -- Join the Mappings to get their Instances   
        LEFT JOIN "Instances" 
        ON "Instances"."InstanceID"="Mappings"."InstanceID"
        
        -- Join the Mappings to get their ScenarioMappings   
        LEFT JOIN "ScenarioMappings"
        ON "ScenarioMappings"."MappingID"="Mappings"."MappingID"
        
        -- Join the ScenarioMappings to get their Scenarios   
        LEFT JOIN "Scenarios"
        ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID"
        
        
        -- Join the Scenarios to get their MasterNetworks   
        LEFT JOIN "MasterNetworks" 
        ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID"
        
        -- Join the Mappings to get their Methods   
        LEFT JOIN "Methods" 
        ON "Methods"."MethodID"="Mappings"."MethodID"
        
        -- Join the Mappings to get their Sources   
        LEFT JOIN "Sources" 
        ON "Sources"."SourceID"="Mappings"."SourceID"
        
        -- Join the Mappings to get their ValuesMappers   
        LEFT JOIN "ValuesMapper" 
        ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID"
        
        -- Join the ValuesMapper to get their MultiAttributeSeries   
        LEFT JOIN "MultiAttributeSeries"  
        ON "MultiAttributeSeries" ."ValuesMapperID"="ValuesMapper"."ValuesMapperID"
        
        
        /*This is an extra join to get to each column name within the MultiColumn Array */
        
        -- Join the MultiAttributeSeries to get to their specific ValuesMapper, now called ValuesMapperColumn
        LEFT JOIN "ValuesMapper" As "ValuesMapperColumn"
        ON "ValuesMapperColumn"."ValuesMapperID"="MultiAttributeSeries"."MappingID_Attribute"
        
        -- Join the ValuesMapperColumn to get back to their specific Mapping, now called MappingColumns
        LEFT JOIN "Mappings" As "MappingColumns"
        ON "MappingColumns"."ValuesMapperID"="ValuesMapperColumn"."ValuesMapperID"
        
        -- Join the MappingColumns to get back to their specific Attribute, now called AttributeColumns
        LEFT JOIN  "Attributes" AS "AttributesColumns"
        ON "AttributesColumns"."AttributeID"="MappingColumns"."AttributeID"
        /* Finishes here */
        
        -- Join the MultiAttributeSeries to get access to their MultiAttributeSeriesValues   
        LEFT JOIN "MultiAttributeSeriesValues"
        ON "MultiAttributeSeriesValues"."MultiAttributeSeriesID"="MultiAttributeSeries"."MultiAttributeSeriesID"
        
        -- Select one InstanceName and restrict the query AttributeDataTypeCV that is MultiAttributeSeries   
        
        WHERE  Attributes.AttributeDataTypeCV='MultiAttributeSeries'  and DataValue is not null
        
        AND ObjectType= '%s' 
    
        AND MultiAttributeName='%s'
        AND InstanceName='%s' 
        
        -- Sort the the values of each column name based on their ascending order
    
    
        ORDER BY ResourceType,ObjectType,InstanceName,ScenarioName,AttributeName,MultiAttributeName,ValueOrder ASC
        
    """%(input_param['Required_ObjectType'],  input_param['Required_AttributeName'], input_param['Provided_InstanceName'] )


        # df_MultiColumns = session.execute(MultiAttributes_query)
        df_MultiColumns = pd.read_sql_query(MultiAttributes_query, conn)

        # df_MultiColumnsKeys = df_MultiColumns.keys()

        total_df_MultiColumns.append(df_MultiColumns)

        Full_Branch=input_param['Provided_FullBranch']
        Multi_Full_Branch_total.append(Full_Branch)

    return (total_df_MultiColumns,Multi_Full_Branch_total)


def MultiAttributes_csv_file(total_df_MultiColumns,Multi_Full_Branch_total):

    # Write
    # the order is important
    # csv_file_name=VolumeElevation( 0, 4590, 130, 4600, 649, 4610, 1739, 4620, 3456, 4630, 5937, 4640, 9236, 4650, 13206, 4660, 17721, 4670, 18684, 4672, 22600, 4680, 28100, 4690, 34100, 4700, 40700, 4710, 47900, 4720, 55800, 4730, 64500, 4740, 73900, 4750 )
    total_csv_file_multi_columns = []
    Multi_df_MultiColumns = []
    Metadata_multi_att=[]
    total_multi_attribute_value=[]

    output_dir = "Multi_Attributes_csv_files/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for df_MultiColumns,Multi_Full_Branch in zip (total_df_MultiColumns,Multi_Full_Branch_total):
        first_index = 0
        if len(df_MultiColumns['ValueOrder']) < 1: continue
        first_order_value = df_MultiColumns['ValueOrder'][0]
        second_index = 0
        i = 0
        n = 0
        # print df_MultiColumns['ValueOrder']
        for order_data in df_MultiColumns['ValueOrder']:
            if i == 0:
                i += 1
                continue
            if order_data == first_order_value:
                second_index = i
                n = second_index
                break
            i += 1

        # diff = second_index - first_index
        MultiParam = ''
        # print n

        for j in range(n):
            try:
                first_data = df_MultiColumns['DataValue'][j]
                second_data = df_MultiColumns['DataValue'][j + n]

                MultiParam += '{},{}'.format(second_data, first_data)
                if j != n - 1:
                    MultiParam += ','
            except:
                break
        # print MultiParam

        # AttributeName(Value),AttributeName(Value)
        # MultiParam=

        csv_file_path_or_value_multi = "VolumeElevation(" + MultiParam + ")"


        # print csv_file_path_or_value_multi

        # csv_file_name=VolumeElevation( 0, 4590, 130, 4600, 649, 4610, 1739, 4620, 3456, 4630, 5937, 4640, 9236, 4650, 13206, 4660, 17721, 4670, 18684, 4672, 22600, 4680, 28100, 4690, 34100, 4700, 40700, 4710, 47900, 4720, 55800, 4730, 64500, 4740, 73900, 4750 )

        Multi_df_MultiColumns.append(df_MultiColumns)

        # reuse the script athe link to print these to a csv file
        # https://github.com/WamdamProject/WaMDaM_Wizard/blob/master/src_1.0/controller/wamdamAPI/GetDataValues.py#L319

        x = df_MultiColumns['AttributeName'][1]
        y = df_MultiColumns['InstanceName'][1]
        z = x.replace(" ", "_")
        w = y.replace(" ", "_")


        csv_file_multi_columns = output_dir + z + '_' + w + '.csv'

        Metadata_multi_att1 = OrderedDict()

        Metadata_multi_att1['FullBranch'] =Multi_Full_Branch
        Metadata_multi_att1['Value'] =csv_file_path_or_value_multi
        Metadata_multi_att1['csv_fileName'] =csv_file_multi_columns

        Metadata_multi_att.append(Metadata_multi_att1)

        # print csv_file_seasonal_multi_columns

        # # save the the multi columns into a csv file with a name csv_file_name
        field_names = ['ObjectType', 'InstanceName', 'ScenarioName', 'MultiAttributeName', 'AttributeDataTypeCV',
                       df_MultiColumns['AttributeName'][first_index], df_MultiColumns['AttributeName'][second_index],
                       'ValueOrder', 'Date exported to this file']

        f2 = open(csv_file_multi_columns, "wb")
        writer1 = csv.writer(f2, delimiter=',', quoting=csv.QUOTE_ALL)
        writer1.writerow(field_names)
        Date_exported = datetime.datetime.now()

        for j in range(n):
            try:
                field_values = [df_MultiColumns['ObjectType'][j], df_MultiColumns['InstanceName'][j],
                                df_MultiColumns['ScenarioName'][j], df_MultiColumns['MultiAttributeName'][j],
                                df_MultiColumns['AttributeDataTypeCV'][j], df_MultiColumns['DataValue'][j],
                                df_MultiColumns['DataValue'][j + n], df_MultiColumns['ValueOrder'][j],Date_exported.strftime('%m/%d/%Y')]
                writer1.writerow(field_values)
            except:
                break

        f2.close()

        # combne many output paramters here to pass them to the metadata wirtting file


    return Multi_df_MultiColumns,Metadata_multi_att
