# this file exports all the data values for all the attributes and instances within
# a scenaro in a master network in a resource type

# input here is as selected in the dlg box to Export WaMDaM to Excel
# selectedResourceType
# selectedNetwork
# selectedScenario

# call this file when we export Values from Export to Excel



import pandas as pd
from ..ConnectDB_ParseExcel import DB_Setup
from ..ConnectDB_ParseExcel import SqlAlchemy as sq

'''
    This class is used to get result that query to get data of values in sqlite db.
'''

class GetAllValuesByScenario(object):
    def __init__(self, pathOfSqlite=''):
        self.setup = DB_Setup()
        if self.setup.get_session() == None and pathOfSqlite != '':
            self.setup.connect(pathOfSqlite, db_type='sqlite')

        self.session = self.setup.get_session()

        self.excel_pointer = None

    def GetAllNumericValues(self, selectedResourceType='', selectedNetwork='', selectedScenario=''):
        '''
        This method is used to get data making NumericValues_table.
        :param selectedType: selected Model Type
        :param selectedAttribute: controlled dNetwork
        :param selectedInstance: controlled Scenarior
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            NumericValues_sql ="""
            SELECT ObjectType, InstanceName,ScenarioName,AttributeName,SourceName,MethodName ,NumericValue
                  FROM "ResourceTypes" 
                  Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" 
                  Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" 
                  Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" 
                  Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" 
                  Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" 
                  Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" 
                  Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" 
                  Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" 
                  Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" 
                  Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" 
                  LEFT JOIN NumericValues ON NumericValues."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" 
		          WHERE AttributeDataTypeCV="NumericValues" AND
                  "ResourceTypeAcronym" = '{}' AND "MasterNetworkName" = '{}' AND "ScenarioName" = '{}'""".format(selectedResourceType, selectedNetwork, selectedScenario)


            NumericValues_Result_df_columns = list(self.session.execute(NumericValues_sql).keys())

            NumericValues_Result_df = pd.DataFrame(list(self.session.execute(NumericValues_sql)))

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if NumericValues_Result_df.empty:
                NumericValues_Result_df=pd.DataFrame(columns=NumericValues_Result_df_columns)
            else:
                NumericValues_Result_df.columns = NumericValues_Result_df_columns

            return NumericValues_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetAllNumericValues.\n' + e.message)





    def GetAllCategoricalValues(self, selectedResourceType='', selectedNetwork='', selectedScenario=''):
        '''
        This method is used to get data making FreeTextSheet.
        :param selectedType: selected Model Type
        :param selectedAttribute: controlled Network
        :param selectedInstance: controlled Scenarior
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            Categorical_sql =""" SELECT ObjectType, InstanceName,ScenarioName,AttributeName,SourceName,MethodName ,CategoricalValue,CategoricalValueCV

                  FROM "ResourceTypes" 
		    
                  Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" 
                  Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" 
                  Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" 
                  Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" 

                  Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" 
                  Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" 
                  Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" 
                  Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" 
                  Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" 
                  Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" 
                  LEFT JOIN CategoricalValues ON CategoricalValues."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" 
                  
		        WHERE AttributeDataTypeCV="CategoricalValues" 
		       AND "ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"
            """.format(selectedResourceType, selectedNetwork, selectedScenario)

            CategoricalValues_Result_df_columns = list(self.session.execute(Categorical_sql).keys())

            CategoricalValues_Result_df = pd.DataFrame(list(self.session.execute(Categorical_sql)))

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if CategoricalValues_Result_df.empty:
                CategoricalValues_Result_df=pd.DataFrame(columns=CategoricalValues_Result_df_columns)
            else:
                CategoricalValues_Result_df.columns = CategoricalValues_Result_df_columns



            return CategoricalValues_Result_df

        except Exception as e:
        # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetAllCategoricalValues.\n' + e.message)



    def GetAllTextFree(self, selectedResourceType='', selectedNetwork='', selectedScenario=''):
        '''
        This method is used to get data making FreeTextSheet.
        :param selectedType: selected Model Type
        :param selectedAttribute: controlled Network
        :param selectedInstance: controlled Scenarior
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:
            TextFree_sql = """ SELECT ObjectType, InstanceName,ScenarioName,AttributeName,SourceName,MethodName ,FreeTextValue

                  FROM "ResourceTypes" 
		            Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" 
                  Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" 
                  Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" 
                  Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" 

                  Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" 
                  Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" 
                  Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" 
                  Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" 
                  Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" 
                  Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" 
                  LEFT JOIN "FreeText" ON "FreeText"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID"
                  
		        WHERE AttributeDataTypeCV="FreeText" 
            		       AND "ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"
                        """.format(selectedResourceType, selectedNetwork, selectedScenario)

            TextFreeValues_Result_df = pd.DataFrame(list(self.session.execute(TextFree_sql)))

            TextFreeValues_Result_df_columns = list(self.session.execute(TextFree_sql).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if TextFreeValues_Result_df.empty:
                TextFreeValues_Result_df=pd.DataFrame(columns=TextFreeValues_Result_df_columns)
            else:
                TextFreeValues_Result_df.columns = TextFreeValues_Result_df_columns

            return TextFreeValues_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetAllTextFree.\n' + e.message)




    def GetAllSeasonalNumericValues(self, selectedResourceType='', selectedNetwork='', selectedScenario=''):
        '''
        This method is used to get data making SeasonalParameter.
        :param selectedResourceType: selected Model name
        :param selectedNetwork: selected Master Network name
        :param selectedScenario: selected scenario Name
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            SeasonalNumericValues_sql ="""
            SELECT ObjectType, InstanceName,ScenarioName,AttributeName, SourceName,MethodName,SeasonName,
            SeasonNameCV, SeasonNumericValue,SeasonOrder,SeasonDateFormate 
                                  FROM "ResourceTypes" 
		         Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" 
                  Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" 
                  Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" 
                  Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" 
                  Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" 
                  Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" 
                  Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" 
                  Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" 
                  Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" 
                  Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" 
                  LEFT JOIN "SeasonalNumericValues" ON "SeasonalNumericValues"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" 		    
                  WHERE "AttributeDataTypeCV"="SeasonalNumericValues" 
            	  AND "ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"
                  ORDER BY SeasonOrder ASC
                        """.format(selectedResourceType, selectedNetwork, selectedScenario)

            SeasonalNumericValues_Result_df = pd.DataFrame(list(self.session.execute(SeasonalNumericValues_sql)))
            SeasonalNumericValues_Result_df_columns = list(self.session.execute(SeasonalNumericValues_sql).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if SeasonalNumericValues_Result_df.empty:
                SeasonalNumericValues_Result_df=pd.DataFrame(columns=SeasonalNumericValues_Result_df_columns)
            else:
                SeasonalNumericValues_Result_df.columns = SeasonalNumericValues_Result_df_columns

            return SeasonalNumericValues_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetAllSeasonalNumericValues.\n' + e.message)

    def GetAllTimeSeries(self, selectedResourceType, selectedNetwork, selectedScenario):
        '''
        This method is used to get data making TimeSeries.
        :param selectedResourceType: selected Model name
        :param selectedNetwork: selected Master Network name
        :param selectedScenario: selected scenario Name
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            TimeSeries_sql = """
               SELECT  DISTINCT ObjectType, InstanceName,ScenarioName,AttributeName, SourceName, MethodName,YearType,
                    AggregationStatisticCV, AggregationInterval, IntervalTimeUnitCV,
                     IsRegular, NoDataValue, TimeSeries.Description As Description
                     
			          FROM "ResourceTypes" 
                     Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" 
                     Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" 
                     Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" 
                     Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" 
                     Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" 
                     Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" 
                     Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" 
                     Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" 
                     Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" 
                     Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" 
                     LEFT JOIN "TimeSeries" ON "TimeSeries"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" 
                     LEFT JOIN "TimeSeriesValues" ON "TimeSeriesValues"."TimeSeriesID" = "TimeSeries"."TimeSeriesID" 
                     WHERE AttributeDataTypeCV="TimeSeries" 
                     AND "ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = '{}'""".format(
                selectedResourceType, selectedNetwork, selectedScenario)

            TimeSeries_Result_df = pd.DataFrame(list(self.session.execute(TimeSeries_sql)))
            TimeSeries_Result_df_columns = list(self.session.execute(TimeSeries_sql).keys())

            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if TimeSeries_Result_df.empty:
                TimeSeries_Result_df=pd.DataFrame(columns=TimeSeries_Result_df_columns)
            else:
                TimeSeries_Result_df.columns = TimeSeries_Result_df_columns

            return TimeSeries_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetAllTimeSeries.\n' + e.message)

    def GetAllTimeSeriesValues(self, selectedResourceType, selectedNetwork, selectedScenario):
        '''
        This method is used to get data making TimeSeries.
        :param selectedResourceType: selected Model name
        :param selectedNetwork: selected Master Network name
        :param selectedScenario: selected scenario Name
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            TimeSeriesValues_sql = """
            SELECT  ObjectType, InstanceName,ScenarioName,AttributeName, "TimeSeriesValues"."DateTimeStamp" ,
            "TimeSeriesValues"."DataValue",SourceName,MethodName
                  FROM "ResourceTypes" 
                  Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" 
                  Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" 
                  Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" 
                  Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" 
                  Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" 
                  Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" 
                  Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" 
                  Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" 
                  Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" 
                  Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" 
                  LEFT JOIN "TimeSeries" ON "TimeSeries"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" 
                  LEFT JOIN "TimeSeriesValues" ON "TimeSeriesValues"."TimeSeriesID" = "TimeSeries"."TimeSeriesID" 
                  WHERE AttributeDataTypeCV="TimeSeries"  
                   AND DateTimeStamp is not NULL 
                   AND ResourceTypeAcronym = '{}' AND MasterNetworkName = '{}' AND ScenarioName = '{}'""".format(selectedResourceType, selectedNetwork, selectedScenario)

            TimeSeriesValues_Result_df = pd.DataFrame(list(self.session.execute(TimeSeriesValues_sql)))
            TimeSeriesValues_Result_df_columns = list(self.session.execute(TimeSeriesValues_sql).keys())





            # get the headers only if the query result is empty. Will use the headers to print them to excel
            if TimeSeriesValues_Result_df.empty:
                TimeSeriesValues_Result_df=pd.DataFrame(columns=TimeSeriesValues_Result_df_columns)
            else:
                TimeSeriesValues_Result_df.columns = TimeSeriesValues_Result_df_columns
                # TimeSeriesValues_Result_df['DateTimeStamp'] = pd.to_datetime(
                #     TimeSeriesValues_Result_df.DateTimeStamp).apply(lambda x: x.strftime('%m/%d/%Y'))
            return TimeSeriesValues_Result_df

        except Exception as e:
            # define.logger.error('Failed metAData load.\n' + e.message)
            raise Exception('Error occurred in reading GetAllTimeSeriesValues.\n' + e.message)





    def GetAllMultiAttributeSeries(self, selectedResourceType='', selectedNetwork='', selectedScenario=''):
        '''
        This method is used to get data making MultiVariableSeries.
        :param selectedResourceType: selected Model name
        :param selectedNetwork: selected Master Network name
        :param selectedScenario: selected scenario Name
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

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
                    
                    AND "ResourceTypeAcronym"="{}"
                    AND "MasterNetworkName"= "{}"
                    AND "ScenarioName" ="{}"
                    
                    ORDER BY InstanceName, ScenarioName,Multi_AttributeName ASC,Sub_AttributeName DESC,ValueOrder ASC
                    """.format(selectedResourceType, selectedNetwork, selectedScenario)

            # Multi_columns_Result_df = pd.DataFrame(list(self.session.execute(sql_Multi_colums)))
            # Multi_columns_Result_df_columns = list(self.session.execute(sql_Multi_colums).keys())
            #
            # # get the headers only if the query result is empty. Will use the headers to print them to excel
            # if  Multi_columns_Result_df.empty:
            #     Multi_columns_Result_df=pd.DataFrame(columns=Multi_columns_Result_df_columns)
            # else:
            #     Multi_columns_Result_df.columns = Multi_columns_Result_df_columns
            #
            # p = Multi_columns_Result_df.pivot(index='', columns='Sub_AttributeName', values='DataValue')
            # new_df=p
            # return Multi_columns_Result_df

            Multi_colums_result = self.session.execute(sql_Multi_colums)


            '''Down Table(MultiVariableSeries_table Table) write'''
            complete_result = list()
            strAtrributName = ''
            valueOrder = None
            Multi_AttributeName = ''
            tempColumn = {}
            sourceName = ''
            i = 0
            currentrow = 0
            setNumber = 0
            for row in Multi_colums_result:
                if row.Multi_AttributeName == None or row.Multi_AttributeName == "":
                    continue

                if strAtrributName != row.Multi_AttributeName:
                    strAtrributName = row.Multi_AttributeName
                    if not row.Multi_AttributeName in tempColumn.keys() :
                        tempColumn[row.Multi_AttributeName] = []
                        tempColumn[row.Multi_AttributeName].append(row['Sub_AttributeName'])
                    Multi_AttributeName = row['Sub_AttributeName']

                    setNumber = i
                if sourceName != row.InstanceName:
                    sourceName = row.InstanceName
                    setNumber = i
                    currentrow = 0
                if Multi_AttributeName != row['Sub_AttributeName']:
                    Multi_AttributeName = row['Sub_AttributeName']
                    currentrow = 0
                # else:
                if row['Sub_AttributeName'] in tempColumn[row.Multi_AttributeName]:
                    index = tempColumn[row.Multi_AttributeName].index(row['Sub_AttributeName'])
                    if index == 0:
                        complete_result.append(
                            [row.ObjectType, row.InstanceName, row.ScenarioName, row.Multi_AttributeName,
                             row.SourceName,
                             row.MethodName, row.DataValue])
                        i += 1
                    else:
                        try:
                            complete_result[setNumber + currentrow].append(row.DataValue)
                            if len(complete_result[setNumber + currentrow]) > 11:
                                pass
                            currentrow += 1
                        except:
                            # currentrow -= 1
                            pass
                else:
                    currentrow = 0
                    tempColumn[row.Multi_AttributeName].append(row['Sub_AttributeName'])
                    index = tempColumn[row.Multi_AttributeName].index(row['Sub_AttributeName'])
                    if index == 0:
                        complete_result.append(
                            [row.ObjectType, row.InstanceName, row.ScenarioName, row.Multi_AttributeName,
                             row.SourceName,
                             row.MethodName, row.DataValue,row.ValueOrder])
                        i += 1
                    else:
                        try:
                            complete_result[setNumber + currentrow].append(row.DataValue)
                            if len(complete_result[setNumber + currentrow]) > 11:
                                pass
                            currentrow += 1
                        except:
                            # currentrow -= 1
                            pass

            bottom_table_result = complete_result





            bottom_header = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName']


            '''Up Table(MultiAttributeName_column Table) write'''


            top_header=['MultiAttributeSeriesName']
            up_table_column_result = list()
            for key, columnItems in tempColumn.items():
                temList = list()
                temList.append(key)
                for i, item in enumerate(columnItems):
                    bottom_header_val = 'AttributeName{}_Values'.format(i+1)
                    if not bottom_header_val in bottom_header:
                        bottom_header.append(bottom_header_val)

                    top_header_val = 'AttributeName{}'.format(i + 1)
                    if not top_header_val in top_header:
                        top_header.append(top_header_val)

                    temList.append(item)
                up_table_column_result.append(temList)


            #append the headers to the df here and then pass the df ready

            up_table_column_result_df=pd.DataFrame(up_table_column_result)
            if len(up_table_column_result) > 0:
                up_table_column_result_df.columns = top_header

            #append the headers to the df here and then pass the df ready

            bottom_table_result_df=pd.DataFrame(bottom_table_result)
            if len(bottom_table_result) > 0:
                bottom_table_result_df.columns = bottom_header

            return up_table_column_result_df,bottom_table_result_df

        except Exception as  e:
            print e
            raise Exception('Error occured in reading GetAllMultiAttributeSeries.\n' + e.message)


