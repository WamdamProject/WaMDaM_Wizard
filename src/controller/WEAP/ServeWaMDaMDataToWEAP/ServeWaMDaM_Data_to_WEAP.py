
# call these  functions from here. the result will save excel data in the second function of each.
from QueryMultiAttributes import *
from QueryTimeSeries import *
from QueryDescriptor import *
from QuerySeasonal import *
from QueryNumeric import *


from controller.ConnectDB_ParseExcel import DB_Setup

from controller.ConnectDB_ParseExcel import SqlAlchemy as sq
from sqlalchemy.orm import aliased

from controller.ConnectDB_ParseExcel import SqlAlchemy as sq
from sqlalchemy.orm import aliased

import sqlite3
import pandas as pd
import win32com.client

# fileDir = ""
# weap_export = WEAP_export(textCtrl_AreaNameOnText, fileDir)

# WEAP=win32com.client.Dispatch("WEAP.WEAPApplication")

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

class ServeWaMDaM_Data_to_WEAP:
    def __init__(self, weap, model, wamdam_network, wamdam_scenario, weap_area, weap_scenario, pathOfSqlite=''):
        self.weap = weap
        self.model = model
        self.wamdam_network = wamdam_network
        self.wamdam_scenario = wamdam_scenario
        self.weap_area = weap_area
        self.weap_scenario = weap_scenario
        self.WEAPAreasDirectory = self.weap.AreasDirectory+weap_area+"\\"+weap_scenario+"_ScenarioData"

        self.setup = DB_Setup()
        if self.setup.get_session() == None and pathOfSqlite != '':
            self.setup.connect(pathOfSqlite, db_type='sqlite')

        self.session = self.setup.get_session()


    def load_data(self):
        self.QueryWaMDaMStructure_Instances(self.weap, self.model, self.wamdam_network, self.wamdam_scenario)


####################################################
# Query WaMDaM list of object types, and their attributes
# for the selected WEAP model
####################################################

    def QueryWaMDaMStructure_Instances(self, WEAP,model='', wamdam_network='', wamdam_scenario=''):


        WEAP_structure_instances_query = """
        SELECT DISTINCT  ObjectType,AttributeName,AttributeName_Abstract,AttributeDataTypeCV,
        UnitName,ScenarioName,InstanceName,Instances.Description as FullBranch
        
        FROM ResourceTypes
        
        LEFT JOIN "ObjectTypes"
        ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID"
        
        LEFT JOIN  "ObjectCategories"
        ON "ObjectCategories"."ObjectCategoryID"="ObjectTypes"."ObjectCategoryID"
        
        LEFT JOIN  "Attributes"
        ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID"
        
        LEFT JOIN "Mappings"
        ON "Mappings"."AttributeID"= "Attributes"."AttributeID"
        
        LEFT JOIN "Instances" 
        ON "Instances"."InstanceID"="Mappings"."InstanceID"
        
        LEFT JOIN "ScenarioMappings"
        ON "ScenarioMappings"."MappingID"="Mappings"."MappingID"
        
        LEFT JOIN "Scenarios" 
        ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID"
        
        LEFT JOIN "MasterNetworks" 
        ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID"
        
        LEFT JOIN "ValuesMapper" 
        ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID"
        
        LEFT JOIN "NumericValues" 
        ON "NumericValues"."ValuesMapperID"="ValuesMapper"."ValuesMapperID"
        
        WHERE InstanceName is not null
        
        --exclude the dummy attributes that are just used to connect Object Types with their Instances.
        AND AttributeName!='ObjectTypeInstances'
        
        AND NumericValue is not 0  
        
        AND ModelInputOrOutput is not "Output"
        
        and AttributeDataTypeCV is not "AttributeSeries"
        
            
        AND ResourceTypeAcronym='{}' AND MasterNetworkName='{}' AND ScenarioName='{}' 
        Order by ObjectType,InstanceName,AttributeName_Abstract asc
        """.format(model, wamdam_network, wamdam_scenario)

        WEAP_structure_instances_df = pd.DataFrame(list(self.session.execute(WEAP_structure_instances_query)))
        WEAP_structure_instances_df_columns = list(self.session.execute(WEAP_structure_instances_query).keys())
        WEAP_structure_instances_df.columns = WEAP_structure_instances_df_columns



        multi_timeseries = []
        multi_AttributeSeries = []
        multi_Seasonal = []
        multi_Numeric=[]
        multi_Descriptor=[]
        for row in WEAP_structure_instances_df.iterrows():

            if row[1]['AttributeDataTypeCV']=='TimeSeries':
                multi_timeseries.append(row)

            elif row[1]['AttributeDataTypeCV'] == 'SeasonalNumericValues':
                multi_Seasonal.append(row)

            #
            elif row[1]['AttributeDataTypeCV'] == 'NumericValues':
                multi_Numeric.append(row)


            elif row[1]['AttributeDataTypeCV'] == 'FreeText':
                multi_Descriptor.append(row)
            #
            #
            elif row[1]['AttributeDataTypeCV'] == 'MultiAttributeSeries':
                multi_AttributeSeries.append(row)
            else:
                continue
        conn = self.session
        WEAPAreasDirectory=self.WEAPAreasDirectory
        # Execute the time series function (for both the query and write csv)
        total_df_TimeSeries,Metadata_TimeSeries =self.execute_TimeSeries_query(conn, multi_timeseries)
        print 'exported time series'


        # Execute the seasonal query
        total_df_Seasonal,Metadata_seasonal = self.execute_Seasonal_query(conn, multi_Seasonal)
        print 'exported seasoal'

        # Execute the multi attributes series query
        total_df_MultiColumns,Metadata_multi_att = self.execute_MultiAtt_query(conn, multi_AttributeSeries)
        print 'exported multi'

        # Execute the numeric attributes  query
        total_df_Numeric,Metadata_multi_numeric = self.execute_Numeric_query(conn, multi_Numeric)
        print 'exported numeric'

        # Execute the descriptor attributes  query
        total_df_Descriptor,Metadata_multi_descriptor = self.execute_Descriptor_query(conn, multi_Descriptor)
        print 'exported descriptor'


        # Execute the metadata file
        # if you see this error message: TypeError: zip argument #1 must support iteration. Its because any of these is empty (no data)
        InputFile_list=self.execute_WriteMetadataFile(WEAPAreasDirectory,total_df_TimeSeries,
                                                      total_df_Seasonal,total_df_MultiColumns,
                                                      total_df_Numeric,total_df_Descriptor,
                              Metadata_TimeSeries,Metadata_seasonal,Metadata_multi_att,
                                                      Metadata_multi_numeric,Metadata_multi_descriptor)

        self.load_InputTo_WEAP(WEAP, InputFile_list)



    def execute_TimeSeries_query(self, conn, multi_timeseries):
        # setup = DB_Setup()
        # session = setup.get_session()

        df_TimeSeries = TimeSeries_query(conn,multi_timeseries)
        if df_TimeSeries:
            total_df_TimeSeries,Metadata_TimeSeries =Timeseries_csv_file(df_TimeSeries, self.WEAPAreasDirectory)

            return (total_df_TimeSeries,Metadata_TimeSeries)
        else:
            return (None, None)


    #total_df_TimeSeries
    #
    def execute_MultiAtt_query(self, conn, multi_AttributeSeries):
        # setup = DB_Setup()
        # session = setup.get_session()
        df_MultiColumns = MultiAttributes_query(conn,multi_AttributeSeries)

        total_df_MultiColumns,Metadata_multi_att = MultiAttributes_csv_file(df_MultiColumns, self.WEAPAreasDirectory)


        return (total_df_MultiColumns,Metadata_multi_att)

    #total_df_Seasonal
    # csv_file_path_or_value_seasonal_all
    def execute_Seasonal_query(self, conn, multi_Seasonal):
        # setup = DB_Setup()
        # session = setup.get_session()
        df_Seasonal = Seasonal_query(conn, multi_Seasonal)
        total_df_Seasonal,Metadata_seasonal = Seasonal_csv_file(df_Seasonal, self.WEAPAreasDirectory)

        return (total_df_Seasonal,Metadata_seasonal)

    #
    def execute_Numeric_query(self, conn, multi_Numeric):
        # setup = DB_Setup()
        # session = setup.get_session()
        # df_Numeric = Numeric_query(session)
        total_df_Numeric,Metadata_multi_numeric = Numeric_query(conn, multi_Numeric)

        return (total_df_Numeric, Metadata_multi_numeric)

    #    total_df_Numeric,Metadata_multi_descriptor = execute_Descriptor_query(conn, multi_Descriptor)

    #
    def execute_Descriptor_query(self, conn, multi_Descriptor):
        # setup = DB_Setup()
        # session = setup.get_session()
        # df_Descriptor = Descriptor_query(session)
        total_df_Descriptor,Metadata_multi_descriptor = Descriptor_query(conn, multi_Descriptor)

        return (total_df_Descriptor, Metadata_multi_descriptor)

        # store these as lists (matrix) then pass it to the write it all once into the input file or make


    def execute_WriteMetadataFile(self, WEAPAreasDirectory,total_df_TimeSeries, total_df_MultiColumns,total_df_Seasonal,total_df_Numeric,total_df_Descriptor,
                                  Metadata_TimeSeries,Metadata_seasonal,Metadata_multi_att,Metadata_multi_numeric,Metadata_multi_descriptor ):

        # multi_AttributeSeries
        # from Read_provided_file_query_Required import *
        # from execute_TimeSeries_query import total_csv_file_name
        from ExportWEAP_Input_metadata_file import WriteMetadataFile
        return WriteMetadataFile(WEAPAreasDirectory,total_df_TimeSeries,total_df_MultiColumns,total_df_Seasonal,total_df_Numeric,total_df_Descriptor,
                          Metadata_TimeSeries,Metadata_seasonal,Metadata_multi_att,Metadata_multi_numeric,Metadata_multi_descriptor)



    def load_InputTo_WEAP(self, WEAP,InputFile_list):
        # WEAP.Branch("Supply and Resources\River\Little Bear River\Reservoirs\Hyrum Reservoir").Variable("Volume Elevation Curve").Expression = "VolumeElevation(0.0,4590.0,130.0,4600.0,649.0,4610.0,1739.0,4620.0,3456.0,4630.0,5937.0,4640.0,9236.0,4650.0,13206.0,4660.0,17721.0,4670.0,18684.0,4672.0,22600.0,4680.0,28100.0,4690.0,34100.0,4700.0,40700.0,4710.0,47900.0,4720.0,55800.0,4730.0,64500.0,4740.0,73900.0,4750.0"
        # WEAP.Branch(BranchFullName).Variable(Required_AttributeName).Expression = InputFile

        for InputFile in InputFile_list:
            AttributeName = InputFile['VariableName']
            Value = InputFile['Value']
            InstanceName = InputFile['BranchName']
            if "Headflow" in InstanceName:
                InstanceName = InstanceName.replace(" Headflow", "")
            ObjectType = InputFile['BranchType']
            if ObjectType == 'River Headflow':
                ObjectType = 'River'

            # if ObjectType not in ('River','Reservoir','Demand Site','Flow Requirement','River Reach'):
            # if ObjectType in ('River Reach'):
                #     and AttributeName in ('Groundwater Outflow','Surface Water Inflow') and \
                # InstanceName in ('Below Bear River Canal Company Return','Below Last Chance Canal Co Return',
                #                 'Below Logan River Inflow','Below Newton Creek Inflow'):

                # As an alternative to using the BranchName from WaMDaM, you can look up the full branch name from WEAP
                # using the existing Instance name (node or link in WEAP)
                # It would work fine for most of the Object types but could be tricky for the reaches


            if ObjectType=="WEAP Global Attributes":
                for Branch in WEAP.Branches:
                    FullBranchName = Branch.FullName
                    BranchName=Branch.Name

                    if "Key\\" in FullBranchName:
                        print FullBranchName

                        if AttributeName==BranchName:
                            for V in Branch.Variables:
                                V.Expression = '0'
                                V.Expression = Value

                    WEAP.ActiveArea.Save

            else:
                for Branch in WEAP.Branches:
                    FullBranchName = Branch.FullName
                    WEAP_BranchTypeName = Branch.TypeName
                    WEAP_BranchName = Branch.Name

                    if WEAP_BranchTypeName == ObjectType and WEAP_BranchName == InstanceName:# and ('Central Bear' or 'Lower Bear' or 'Cub' or 'Malad' or 'Deep' or 'Mink') in FullBranchName:
                        print FullBranchName
                        # print Value
                        if WEAP.Branch(FullBranchName).Variables.Exists(AttributeName):
                            if not AttributeName == 'Method':
                                WEAP.Branch(FullBranchName).Variable(AttributeName).Expression = '0'
                                WEAP.Branch(FullBranchName).Variable(AttributeName).Expression = Value
            WEAP.ActiveArea.Save

            # Execute loading data to WEAP
            # load_InputTo_WEAP(WEAP,InputFile_list)
            Save=WEAP.ActiveArea.Save
            Save =WEAP.SaveArea

        print 'Done loading to WEAP'
        print 'Saved'