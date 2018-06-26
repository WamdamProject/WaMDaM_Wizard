
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
        AttributeName,AttributeDataTypeCV,
         "Instances"."InstanceName" As NodeORLinkInstanceName,
        UnitName,DescriptorValue
            
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
        LEFT JOIN "DescriptorValues"
        ON "DescriptorValues"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID"
        
        ---------------------------------------------------------------------------------------------
        -- Join the Connections table to the Instances table   
        LEFT JOIN "Connections" 
        ON "Connections"."LinkInstanceID"="Instances"."InstanceID"
        
        -- Join the Instances table the End Node of link   
        LEFT JOIN "Instances" As "EndNodeInstance"
        ON "EndNodeInstance"."InstanceID"="Connections"."EndNodeInstanceID"
        
        -- Join the Instances table the Start Node of link   
        LEFT JOIN "Instances" As "StartNodeInstance"
        ON "StartNodeInstance"."InstanceID"="Connections"."StartNodeInstanceID"
        ---------------------------------------------------------------------------------------------
        
        WHERE  
        
        AttributeDataTypeCV IN ('DescriptorValues' ) and DescriptorValue is not null

        AND ObjectType= '%s' 
    
        AND AttributeName='%s'
        AND NodeORLinkInstanceName='%s'     
        
        """%(input_param['Required_ObjectType'], input_param['Required_AttributeName'], input_param['Provided_InstanceName'] )

        df_Descriptor = pd.read_sql_query(Descriptor_query, conn)

        # df_Descriptor = session.execute(Descriptor_query)

        df_Descriptor = pd.read_sql_query(Descriptor_query, conn)


        Full_Branch=input_param['Provided_FullBranch']

        if len (df_Descriptor['AttributeName']) == 0 : continue

        df_Descriptor['Value']=df_Descriptor['DescriptorValue']

        total_df_Descriptor.append(df_Descriptor)

        Metadata_multi_descriptor1 = OrderedDict()

        Metadata_multi_descriptor1['FullBranch'] =Full_Branch

        Metadata_multi_descriptor1['csv_fileName'] =''

        Metadata_multi_descriptor.append(Metadata_multi_descriptor1)


    return total_df_Descriptor, Metadata_multi_descriptor
