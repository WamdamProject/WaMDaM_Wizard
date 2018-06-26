
from collections import OrderedDict
import pandas as pd
from controller.WEAP_exporter import Extract_Network

# Option 1: query network based on the provided name in the GUI

def GetWASH_net_SearchValues(unique_object_types_value_list,BranchesNew_list):
    exclude_object_type_list = ['Return Flow Node', 'River Withdrawal', 'Tributary Inflow', 'River Mouth']
    # loop over all the WEAP Object Types and exclude the above ones (they dont take input data so no need to search for them)

    for Objects in BranchesNew_list:
        for unique_object_types_value in unique_object_types_value_list:
            if unique_object_types_value in exclude_object_type_list:
                continue

    # Save them to Excel
    field_names = ['ObjectType', 'ObjectTypology','InstanceName','InstanceNameCV','FullBranch']


    
# Option 2: Read network from a provided excel file

# Read the excel file

    Network_input = pd.read_excel('./Network_input.xlsm', sheetname=None)

    Network_input.keys()


    Provided_ObjectType
    Provided_InstanceName
    Provided_FullBranch

    # based on the selected model (WEAP) or (WASH),

    ModelName='WASH'

    #Query WaMDaM db to get the list of Object types and their Attributes

    Model_required_attributes='''
    SELECT DISTINCT  ObjectType as Required_ObjectType,ObjectTypeCV as Required_ObjectTypeCV ,
    AttributeName as Required_AttributeName, AttributeNameCV Required_AttributeNameCV, 
    AttributeDataTypeCV as Required_AttributeDataTypeCV, UnitName as Required_UnitName
    
    FROM ResourceTypes
    
    LEFT JOIN "ObjectTypes" 
    ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID"
    
    LEFT JOIN  "ObjectCategories"
    ON "ObjectCategories"."ObjectCategoryID"="ObjectTypes"."ObjectCategoryID" 
    
    LEFT JOIN  "Attributes"
    ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" 
    
    LEFT JOIN  "AttributeCategories"
    ON "AttributeCategories"."AttributeCategoryID"="Attributes"."AttributeCategoryID" 
    
    -- Provide the model name 
    WHERE "ResourceTypeAcronym"='WEAP' --ModelName
    --WHERE "ResourceTypeAcronym"='WASH' 
    
    --exclude the dummy attributes that are just used to connect Object Types with their Instances. 
    AND AttributeName!='ObjectTypeInstances' 
    '''


    df_Model_required_attributes= session.execute(Model_required_attributes)


    Model_required_attributes.keys()

    Query_Load_params=[]

    Required_ObjectType
    Required_AttributeName
    Required_AttributeDataTypeCV
    Required_UnitName

    for prov_objs in Provided_ObjectType:
        for req_objs in Required_ObjectType:
            if  prov_objs == req_objs:
                Query_Load_params['Required_AttributeName'] = req_objs[Required_AttributeName]
                Query_Load_params['Required_AttributeDataTypeCV'] = req_objs[Required_AttributeDataTypeCV]
                Query_Load_params['Required_UnitName'] = req_objs[Required_UnitName]
                Query_Load_params['Provided_InstanceName'] = prov_objs[Provided_InstanceName]
                Query_Load_params['Provided_FullBranch'] = prov_objs[Provided_FullBranch]


    return Query_Load_params


# for
# based on the provided Object type in excel, iterate over its defined Attributes in WAMDAM for each Instance

