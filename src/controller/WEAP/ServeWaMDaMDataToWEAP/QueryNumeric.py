
# query Numeric data:
# Input paramters: ObjectTypeCV,InstanceNameCV,AttributeNameCV
# return: df_Numeric

import pandas as pd
from collections import OrderedDict

 # for the model (Distination)

def Numeric_query(conn,multi_Numeric):
    Metadata_multi_numeric=[]
    total_df_Numeric=[]

    for input_param in multi_Numeric:

        Numeric_query="""
        Select ScenarioName,ObjectTypeCV,ObjectType,AttributeName_Abstract,AttributeDataTypeCV,InstanceName,
        UnitName,MethodName,SourceName,
         --As Existing_UnitName,
         NumericValue,'' as Converted_NumericValue
    
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
        
        
        -- Join the ValuesMapper to get their Numeric parameters   
        LEFT JOIN "NumericValues"
        ON "NumericValues"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID"
        
        
        WHERE  
        
        
        AttributeDataTypeCV IN ('NumericValues' ) and NumericValue is not null
        
        AND ObjectType= '%s' 
        AND AttributeName_Abstract='%s'
        AND InstanceName='%s' 
                  
                    AND ScenarioName='%s' 

    """%(input_param[1]['ObjectType'],  input_param[1]['AttributeName_Abstract'],
         input_param[1]['InstanceName'],input_param[1]['ScenarioName'] )


        df_Numeric = pd.DataFrame(list(conn.execute(Numeric_query)))

        Numeric_query_columns = list(conn.execute(Numeric_query).keys())
        df_Numeric.columns = Numeric_query_columns

        # if len (df_Numeric['AttributeName_Abstract']) == 0 : continue
        df_Numeric['Value']=df_Numeric['NumericValue']

        total_df_Numeric.append(df_Numeric)

    # convert unit from the existing into the required (or distination)

        # Existing_UnitName=df_Numeric['Existing_UnitName']
        # Required_UnitName=input_param['Required_UnitName']

        # if Existing_UnitName==Required_UnitName:
        #     ConversionFactor=1
        # else:
        #     ConversionFactor=1


        # df_Numeric['Converted_NumericValue']=df_Numeric['NumericValue']#*ConversionFactor
        #
        # total_df_MultiColumns.append(df_Numeric)

        Metadata_multi_numeric1 = OrderedDict()


        Metadata_multi_numeric1['csv_fileName'] =''

        Metadata_multi_numeric.append(Metadata_multi_numeric1)

    return total_df_Numeric, Metadata_multi_numeric
