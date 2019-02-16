
# call these  functions from here. the result will save excel data in the second function of each.
from QueryMultiAttributes import *
from QueryTimeSeries import *
from QueryDescriptor import *
from QuerySeasonal import *
from QueryNumeric import *


from controller.ConnectDB_ParseExcel import DB_Setup

from controller.ConnectDB_ParseExcel import SqlAlchemy as sq
from sqlalchemy.orm import aliased

import sqlite3
import pandas as pd
import win32com.client

# fileDir = ""
# weap_export = WEAP_export(textCtrl_AreaNameOnText, fileDir)

WEAP=win32com.client.Dispatch("WEAP.WEAPApplication")

# textCtrl_AreaNameOnText = "BearRiverFeb2018_V1"
#
# ActiveArea = WEAP.ActiveArea.Name
# Scenario = WEAP.ActiveScenario.Name
#
# WEAPAreasDirectory = WEAP.AreasDirectory
#
# print ActiveArea
# print Scenario
# print WEAPAreasDirectory
# SourceName = WEAP.ActiveArea.Name



def Read_provided_file_query_Required(WEAP):

    Network_input = pd.read_excel('./Network_input.xlsx', sheetname=None)
    sheetnames = Network_input.keys()
    sheet = Network_input[sheetnames[0]]

    keys = sheet.columns
    query_data_list = []
    # for column in keys:
    #     query_data_list[column] = []

    for i in sheet.index:
        row = {}
        for column in keys:
            row[column] = sheet[column][i]
        query_data_list.append(row)

    # print query_data_list



    # based on the selected model (WEAP) or (WASH),

    ModelName = 'WEAP'

    # Query WaMDaM db to get the list of Object types and their Attributes

    Model_required_attributes = '''
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
    WHERE "ResourceTypeAcronym"='%s'

    --exclude the dummy attributes that are just used to connect Object Types with their Instances.
    AND AttributeName!='ObjectTypeInstances'
    '''%(ModelName)
    # df_Model_required_attributes = session.execute(Model_required_attributes)
    conn = sqlite3.connect("WaMDaM_db.sqlite")

    df_Model_required_attributes = pd.read_sql_query(Model_required_attributes, conn)

    #     Model_required_attributes.keys()
    #
    # Required_ObjectType=df_Model_required_attributes['Required_ObjectType']
    # Required_AttributeName=df_Model_required_attributes['Required_AttributeName']
    # Required_AttributeDataTypeCV=df_Model_required_attributes['Required_AttributeDataTypeCV']
    # Required_UnitName=df_Model_required_attributes['Required_UnitName']


    Query_Load_params_list = []


    # loop over the provided Object Types in Excel.
    # loop over the Required ObjectTypes from the db query
    # If the provided Object Type equals the required object type, then get the
    for prov_objs in query_data_list:
        for i, req_objs in enumerate(df_Model_required_attributes['Required_ObjectType']): # get the string value inside each column
            if prov_objs['Provided_ObjectType'] == req_objs:
                Query_Load_params = {}
                Query_Load_params['Required_AttributeName'] = df_Model_required_attributes['Required_AttributeName'][i]
                Query_Load_params['Required_AttributeDataTypeCV'] = df_Model_required_attributes['Required_AttributeDataTypeCV'][i]
                Query_Load_params['Required_UnitName'] = df_Model_required_attributes['Required_UnitName'][i]
                Query_Load_params['Required_ObjectType'] = req_objs
                Query_Load_params['Provided_ObjectType'] = prov_objs['Provided_ObjectType'] #
                Query_Load_params['Provided_InstanceName'] = prov_objs['Provided_InstanceName']
                Query_Load_params['Provided_FullBranch'] = prov_objs['Provided_FullBranch']
                Query_Load_params_list.append(Query_Load_params)

    # print Query_Load_params_list
    # return Query_Load_params_list

    # iterate over the rows and get the string value of each Required_AttributeDataTypeCV
    setup = DB_Setup()
    session = setup.get_session()

    multi_timeseries = []
    multi_AttributeSeries = []
    multi_Seasonal = []
    multi_Numeric=[]
    multi_Descriptor=[]
    for input_param in Query_Load_params_list:
        if input_param['Required_AttributeDataTypeCV']=='TimeSeries':
            #call the time series function
            #pass the input_param value to the time series function
            multi_timeseries.append(input_param)

        elif input_param['Required_AttributeDataTypeCV'] == 'SeasonalNumericValues':
            multi_Seasonal.append(input_param)

        #
        elif input_param['Required_AttributeDataTypeCV'] == 'NumericValues':
            multi_Numeric.append(input_param)


        elif input_param['Required_AttributeDataTypeCV'] == 'DescriptorValues':
            multi_Descriptor.append(input_param)
        #
        #
        elif input_param['Required_AttributeDataTypeCV'] == 'MultiAttributeSeries':
            multi_AttributeSeries.append(input_param)
        else:
            continue

    # Execute the time series function (for both the query and write csv)
    total_df_TimeSeries,Metadata_TimeSeries =execute_TimeSeries_query(conn, multi_timeseries)


    # Execute the seasonal query
    total_df_Seasonal,Metadata_seasonal = execute_Seasonal_query(conn, multi_Seasonal)


    # Execute the multi attributes series query
    total_df_MultiColumns,Metadata_multi_att = execute_MultiAtt_query(conn, multi_AttributeSeries)


    # Execute the numeric attributes  query
    total_df_Numeric,Metadata_multi_numeric = execute_Numeric_query(conn, multi_Numeric)


    # Execute the descriptor attributes  query
    total_df_Descriptor,Metadata_multi_descriptor = execute_Descriptor_query(conn, multi_Descriptor)


    # Execute the metadata file
    InputFile_list = execute_WriteMetadataFile(total_df_TimeSeries, total_df_Seasonal,total_df_MultiColumns,total_df_Numeric,total_df_Descriptor,
                      Metadata_TimeSeries , Metadata_seasonal,Metadata_multi_att,Metadata_multi_numeric,Metadata_multi_descriptor)


    load_InputTo_WEAP(WEAP, InputFile_list)



def execute_TimeSeries_query(conn, multi_timeseries):
    # setup = DB_Setup()
    # session = setup.get_session()

    df_TimeSeries,TimeSeries_Full_Branch_total = TimeSeries_query(conn,multi_timeseries)

    total_df_TimeSeries,Metadata_TimeSeries =Timeseries_csv_file(df_TimeSeries,TimeSeries_Full_Branch_total)

    return (total_df_TimeSeries,Metadata_TimeSeries)


#total_df_TimeSeries
#
def execute_MultiAtt_query(conn, multi_AttributeSeries):
    # setup = DB_Setup()
    # session = setup.get_session()
    df_MultiColumns,Multi_Full_Branch_total = MultiAttributes_query(conn,multi_AttributeSeries)

    total_df_MultiColumns,Metadata_multi_att = MultiAttributes_csv_file(df_MultiColumns,Multi_Full_Branch_total)


    return (total_df_MultiColumns,Metadata_multi_att)

#total_df_Seasonal
# csv_file_path_or_value_seasonal_all
def execute_Seasonal_query(conn, multi_Seasonal):
    # setup = DB_Setup()
    # session = setup.get_session()
    df_Seasonal,Seasonal_Full_Branch_total = Seasonal_query(conn, multi_Seasonal)
    total_df_Seasonal,Metadata_seasonal = Seasonal_csv_file(df_Seasonal,Seasonal_Full_Branch_total)

    return (total_df_Seasonal,Metadata_seasonal)

#
def execute_Numeric_query(conn, multi_Numeric):
    # setup = DB_Setup()
    # session = setup.get_session()
    # df_Numeric = Numeric_query(session)
    total_df_Numeric,Metadata_multi_numeric = Numeric_query(conn, multi_Numeric)

    return (total_df_Numeric, Metadata_multi_numeric)

#    total_df_Numeric,Metadata_multi_descriptor = execute_Descriptor_query(conn, multi_Descriptor)

#
def execute_Descriptor_query(conn, multi_Descriptor):
    # setup = DB_Setup()
    # session = setup.get_session()
    # df_Descriptor = Descriptor_query(session)
    total_df_Descriptor,Metadata_multi_descriptor = Descriptor_query(conn, multi_Descriptor)

    return (total_df_Descriptor, Metadata_multi_descriptor)



    # store these as lists (matrix) then pass it to the write it all once into the input file or make


def execute_WriteMetadataFile(total_df_TimeSeries, total_df_MultiColumns,total_df_Seasonal,total_df_Numeric,total_df_Descriptor,
                              Metadata_TimeSeries,Metadata_seasonal,Metadata_multi_att,Metadata_multi_numeric,Metadata_multi_descriptor ):

    # multi_AttributeSeries
    # from Read_provided_file_query_Required import *
    # from execute_TimeSeries_query import total_csv_file_name
    from ExportWEAP_Inputfile import WriteMetadataFile
    return WriteMetadataFile(total_df_TimeSeries,total_df_MultiColumns,total_df_Seasonal,total_df_Numeric,total_df_Descriptor,
                      Metadata_TimeSeries,Metadata_seasonal,Metadata_multi_att,Metadata_multi_numeric,Metadata_multi_descriptor)



def load_InputTo_WEAP(WEAP,InputFile_list):
    # WEAP.Branch("Supply and Resources\River\Little Bear River\Reservoirs\Hyrum Reservoir").Variable("Volume Elevation Curve").Expression = "VolumeElevation(0.0,4590.0,130.0,4600.0,649.0,4610.0,1739.0,4620.0,3456.0,4630.0,5937.0,4640.0,9236.0,4650.0,13206.0,4660.0,17721.0,4670.0,18684.0,4672.0,22600.0,4680.0,28100.0,4690.0,34100.0,4700.0,40700.0,4710.0,47900.0,4720.0,55800.0,4730.0,64500.0,4740.0,73900.0,4750.0"
    # WEAP.Branch(BranchFullName).Variable(Required_AttributeName).Expression = InputFile

    for InputFile in InputFile_list:
        BranchName = InputFile['FullBranch']
        # As an alternative to using the BranchName from WaMDaM, you can look up the full branch name from WEAP
        # using the existing Instance name (node or link in WEAP)
        # It would work fine for most of the Object types but could be tricky for the reaches
        Required_AttributeName = InputFile['VariableName']
        Value = InputFile['Value']
        if Required_AttributeName=='Model Water Quality?': continue
        for Branch in WEAP.Branches:
            if Branch.FullName == BranchName:
                for V in Branch.Variables:
                    # check if the provided attribute from WAMDAM matches the one used in WEAP
                    if Required_AttributeName == V.Name:
                        WEAP.Branch(BranchName).Variable(Required_AttributeName).Expression = Value
                        print BranchName,Required_AttributeName,Value
            # if Branch.TypeName=='Demand Site':
            #     for V in Branch.Variables:
        #             if V.Name=='Method' and V.Expression == 'Specify monthly demand':
        #                 InputFile['VariableName']='Monthly Demand'
        # 'Consumption'



        # Execute loading data to WEAP
        # load_InputTo_WEAP(WEAP,InputFile_list)
#           # Option 2: Read network from a provided excel file
#
#     # Read the excel file

Read_provided_file_query_Required(WEAP)