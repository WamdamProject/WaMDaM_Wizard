
import pandas as pd
import sqlite3

WaMDaM_SQLite_Name='WEAP.sqlite'

# WaMDaM_SQLite_Name='replicateWaMDaM.sqlite'


conn = sqlite3.connect(WaMDaM_SQLite_Name)

WaMDaM_SQLite_Name='BearRiverDatasets_August_2018.sqlite'


sql_Multi_colums = """
                   SELECT DISTINCT "ObjectTypes"."ObjectType",
                   "Instances"."InstanceName",
                   ScenarioName,"Attributes"."AttributeName" AS Multi_AttributeName,
                   Methods.MethodName,Sources.SourceName,
                   "AttributesColumns"."AttributeName" AS "Sub_AttributeName",
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

                   WHERE  Attributes.AttributeDataTypeCV='MultiAttributeSeries'  and DataValue is not "" and DataValue is not null                    
                                       --AND Multi_AttributeName='wsi_par'

                   AND "ResourceTypeAcronym"="WASH"
                   AND "MasterNetworkName"= "Lower Bear River Network"
                   AND "ScenarioName" ="base case scenario 2003"

                   ORDER BY InstanceName, ScenarioName,Multi_AttributeName,Sub_AttributeName,ValueOrder ASC
                   """


Multi_colums_result_df=pd.read_sql( sql_Multi_colums , conn)



subsets = Multi_colums_result_df.groupby(['ObjectType', 'InstanceName', 'Multi_AttributeName'])

for subset in subsets.groups.keys():
    dt = subsets.get_group(name=subset)
    attr_name = dt['Multi_AttributeNameAttributeName'].values[3]  # Big attribute
    AttributeNameNos = dt['Sub_AttributeName']  # all small attributes

 for subset in subsets.groups.keys():
            dt = subsets.get_group(name=subset)
            AttributeName1_Values=dt['AttributeName1_Values']
            AttributeName2_Values=dt['AttributeName2_Values']

            ObjectType = dt['ObjectType'].values[0]
            InstanceName = dt['InstanceName'].values[1]
            attr_name = dt['AttributeName'].values[3]

            if (InstanceName, attr_name) in dict_res_attr.keys():
                Attr_name = multiAttr_sheet_bottom_df.values[k][3]
                ObjectType = multiAttr_sheet_bottom_df.values[k][0]
                dimension = Dataset_attr_Name_Dim_list[ObjectType,Attr_name]


                rs_multi = {'resource_attr_id': dict_res_attr[(multiAttr_sheet_bottom_df.values[k][1], multiAttr_sheet_bottom_df.values[k][3])]['id']}

                dataset = {'type': 'array', 'name': multiAttr_sheet_bottom_df.values[k][3], 'unit': attr_unit, 'dimension': dimension,
                                'metadata': json.dumps(metadata, ensure_ascii=True),
                                   'hidden': 'N', 'value': json.dumps(array_value)}
                rs_multi['value'] = dataset
                list_rs_multi.append(rs_multi)