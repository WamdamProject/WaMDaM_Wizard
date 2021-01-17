
# query Descriptor data:
# Input paramters: ObjectTypeCV,InstanceNameCV,AttributeNameCV
# return: df_Descriptor

import pandas as pd
from collections import OrderedDict



def Descriptor_query(conn,multi_Descriptor):
    Metadata_multi_descriptor=[]
    total_df_Descriptor=[]

    for input_param in multi_Descriptor:

        Descriptor_query="""
         Select ScenarioName,ObjectTypeCV,ObjectType,SourceName,MethodName,
        AttributeName_Abstract,AttributeDataTypeCV,InstanceName,UnitName,FreeTextValue
            
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
        
        
        -- Join the ValuesMapper to get their Descriptor parameters   
        LEFT JOIN "FreeText"
        ON "FreeText"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID"
        
        
        WHERE  
        
        AttributeDataTypeCV IN ('FreeText' ) and FreeTextValue is not null
       
       
        AND ObjectType= '%s' 
    
        AND AttributeName_Abstract='%s'
        
        AND InstanceName='%s'     
        
        AND ScenarioName='%s' 

        """%(input_param[1]['ObjectType'], input_param[1]['AttributeName_Abstract'],
             input_param[1]['InstanceName'],input_param[1]['ScenarioName'] )

        df_Descriptor = pd.DataFrame(list(conn.execute(Descriptor_query)))

        df_Descriptor_columns = list(conn.execute(Descriptor_query).keys())
        df_Descriptor.columns = df_Descriptor_columns

        # if len (df_Numeric['AttributeName_Abstract']) == 0 : continue
        df_Descriptor['Value']=df_Descriptor['FreeTextValue']

        total_df_Descriptor.append(df_Descriptor)



        Metadata_multi_descriptor1 = OrderedDict()


        Metadata_multi_descriptor1['csv_fileName'] =''

        Metadata_multi_descriptor.append(Metadata_multi_descriptor1)


    return total_df_Descriptor, Metadata_multi_descriptor
