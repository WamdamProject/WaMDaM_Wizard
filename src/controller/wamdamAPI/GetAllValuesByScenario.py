# this file exports all the data values for all the attributes and instances within
# a scenaro in a master network in a resource type

# input here is as selected in the dlg box to Export WaMDaM to Excel
# selectedResourceType
# selectedNetwork
# selectedScenarior

# call this file when we export Values from Export to Excel




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

    def GetAllNumericValues(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making NumericValues_table.
        :param selectedType: selected Model Type
        :param selectedAttribute: controlled dNetwork
        :param selectedInstance: controlled Scenarior
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            sql = 'SELECT "ResourceTypes"."ResourceType", ObjectType,AttributeName, SourceName, InstanceName,MasterNetworkName,' \
                  'ScenarioName,MethodName, NumericValue ' \
                  'FROM "ResourceTypes" ' \
                  'Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" ' \
                  'Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" ' \
                  'Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" ' \
                  'Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" ' \
                  'Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" ' \
                  'Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" ' \
                  'Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" ' \
                  'Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" ' \
                  'Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" ' \
                  'Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" ' \
                  'LEFT JOIN "NumericValues" ON "NumericValues"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" ' \
                  'WHERE "AttributeDataTypeCV"="NumericValues" AND "ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"' \
                .format(selectedResourceType, selectedNetwork, selectedScenarior)

            result = self.session.execute(sql)
            # nameResult = list()
            complete_result = list()
            for row in result:
                # isExisting = False
                # for name in nameResult:
                #     if name == row.InstanceName:
                #         isExisting = True
                #         break
                # if not isExisting:
                #     nameResult.append(row.InstanceName)
                complete_result.append([row.ObjectType, row.InstanceName, row.ScenarioName,
                                        row.AttributeName, row.SourceName, row.MethodName,
                                        row.NumericValue])

            return complete_result
        except Exception as  e:
            print e
            raise Exception('Error occured in reading Data Structure.\n' + e.message)

    def GetAllCategoricalValues(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making FreeTextSheet.
        :param selectedType: selected Model Type
        :param selectedAttribute: controlled Network
        :param selectedInstance: controlled Scenarior
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            sql =""" SELECT ResourceType, ObjectType, AttributeName, SourceName, InstanceName,CategoricalValue,CategoricalValueCV,
                  ScenarioName,MethodName 
                  FROM "ResourceTypes" 
                  Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" 
                  Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" 
                  Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" 
                  Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" 
		    LEFT JOIN CategoricalValues
		    ON CategoricalValues.ValuesMapperID=ValuesMapper.ValuesMapperID
                  Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" 
                  Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" 
                  Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" 
                  Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" 
                  Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" 
                  Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" 
                  LEFT JOIN "FreeText" ON "FreeText"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" 
                  
		        WHERE AttributeDataTypeCV="CategoricalValues" 
		       AND "ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"
            """.format(selectedResourceType, selectedNetwork, selectedScenarior)

            result = self.session.execute(sql)
            # nameResult = list()
            complete_result = list()
            for row in result:
                complete_result.append([row.ObjectType, row.InstanceName, row.ScenarioName,
                                        row.AttributeName, row.SourceName, row.MethodName,
                                        row.CategoricalValue, row.CategoricalValueCV])
            return complete_result
        except Exception as  e:
            print e
            raise Exception('Error occured in reading the Data Structure.\n' + e.message)

    def GetAllTextFree(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making FreeTextSheet.
        :param selectedType: selected Model Type
        :param selectedAttribute: controlled Network
        :param selectedInstance: controlled Scenarior
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            sql = 'SELECT ResourceType, ObjectType, AttributeName, SourceName, InstanceName,FreeTextValue,' \
                  'ScenarioName,MethodName ' \
                  'FROM "ResourceTypes" ' \
                  'Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" ' \
                  'Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" ' \
                  'Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" ' \
                  'Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" ' \
                  'Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" ' \
                  'Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" ' \
                  'Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" ' \
                  'Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" ' \
                  'Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" ' \
                  'Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" ' \
                  'LEFT JOIN "FreeText" ON "FreeText"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" ' \
                  'WHERE AttributeDataTypeCV="FreeText" ' \
                  ' AND "ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"' \
                .format(selectedResourceType, selectedNetwork, selectedScenarior)

            result = self.session.execute(sql)
            # we need to find a way to make this result


            # nameResult = list()
            complete_result = list()
            for row in result:
                complete_result.append([row.ObjectType, row.InstanceName, row.ScenarioName,
                                        row.AttributeName, row.SourceName, row.MethodName, row.FreeTextValue])
            return complete_result
        except Exception as  e:
            print e

            raise Exception('Erro occure in reading Data Structure.\n' + e.message)


    # def GetAllCategoricalValues(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
    #     '''
    #     This method is used to get data making Parameter.
    #     :param selectedResourceType: selected Model name
    #     :param selectedNetwork: selected Master Network name
    #     :param selectedScenarior: selected scenario Name
    #     :param excelPath: full path of excel file to export data
    #     :return: None
    #     '''
    #     try:
    #         sql = 'SELECT "ResourceTypes"."ResourceType", ObjectType,AttributeName, SourceName, InstanceName,MasterNetworkName,' \
    #               'ScenarioName,MethodName, NumericValue ' \
    #             'FROM "ResourceTypes" '\
    #             'Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" '\
    #             'Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" '\
    #             'Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" '\
    #             'Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" '\
    #             'Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID"'\
    #             'Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" '\
    #             'Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" '\
    #             'Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" '\
    #             'Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" '\
    #             'Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" '\
    #             'LEFT JOIN "NumericValues" ON "NumericValues"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" '\
    #             'WHERE "Attributes"."AttributeDataTypeCV"="SeasonalNumericValues" AND "ResourceTypes"."ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"'\
    #             .format(selectedResourceType, selectedNetwork, selectedScenarior)
    #
    #         result = self.session.execute(sql)
    #         # nameResult = list()
    #         complete_result = list()
    #         for row in result:
    #             # isExisting = False
    #             # for name in nameResult:
    #             #     if name == row.InstanceName:
    #             #         isExisting = True
    #             #         break
    #             # if not isExisting:
    #             #     nameResult.append(row.InstanceName)
    #             complete_result.append([row.ObjectType, row.InstanceName, row.ScenarioName,
    #                                     row.AttributeName, row.SourceName, row.MethodName,
    #                                     row.NumericValue])
    #         return complete_result
    #     except Exception as  e:
    #         print e
    #         raise Exception('Error occurer in reading Data Structure.\n' + e.message)
    #



    def GetAllSeasonalNumericValues(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making SeasonalParameter.
        :param selectedResourceType: selected Model name
        :param selectedNetwork: selected Master Network name
        :param selectedScenarior: selected scenario Name
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            sql ="""SELECT ObjectType, AttributeName, SourceName, InstanceName,MasterNetworkName,
                        ScenarioName,MethodName,SeasonName, SeasonNumericValue, SeasonNameCV, SeasonOrder,SeasonDateFormate 
                  FROM "Attributes" 
                  Left JOIN "ObjectTypes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" 
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
                    AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"
                    """.format(selectedNetwork, selectedScenarior)

            result = self.session.execute(sql)
            # nameResult = list()
            complete_result = list()
            for row in result:
                complete_result.append([row.ObjectType, row.InstanceName, row.ScenarioName,
                                        row.AttributeName, row.SourceName, row.MethodName,
                                        row.SeasonName, row.SeasonNameCV, row.SeasonNumericValue,
                                        row.SeasonDateFormate])
            return complete_result
        except Exception as  e:
            print e
            raise Exception('Erro occure in reading Data Structure.\n' + e.message)

    def GetAllTimeSeries(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making TimeSeries.
        :param selectedResourceType: selected Model name
        :param selectedNetwork: selected Master Network name
        :param selectedScenarior: selected scenario Name
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            sql = 'SELECT ResourceType ObjectType, AttributeName, SourceName, InstanceName,YearType,' \
                  'ScenarioName,MethodName,AggregationStatisticCV, AggregationInterval, IntervalTimeUnitCV,' \
                  'IsRegular, NoDataValue, "TimeSeries"."Description", "TimeSeriesValues"."DataValue", "TimeSeriesValues"."DateTimeStamp" ' \
                  'FROM "ResourceTypes" ' \
                  'Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" ' \
                  'Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" ' \
                  'Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" ' \
                  'Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" ' \
                  'Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" ' \
                  'Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" ' \
                  'Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" ' \
                  'Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" ' \
                  'Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" ' \
                  'Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" ' \
                  'LEFT JOIN "TimeSeries" ON "TimeSeries"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" ' \
                  'LEFT JOIN "TimeSeriesValues" ON "TimeSeriesValues"."TimeSeriesID" = "TimeSeries"."TimeSeriesID" ' \
                  'WHERE AttributeDataTypeCV="TimeSeries" ' \
                  'AND "ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"' \
                .format(selectedResourceType, selectedNetwork, selectedScenarior)

            result = self.session.execute(sql)
            # nameResult = list()
            complete_result = list()
            for row in result:
                # isExisting = False
                # for name in nameResult:
                #     if name == row.InstanceName:
                #         isExisting = True
                #         break
                # if not isExisting:
                #     nameResult.append(row.InstanceName)
                complete_result.append([row.ObjectType, row.InstanceName, row.ScenarioName,
                                        row.AttributeName, row.DateTimeStamp, row.DataValue])
            return complete_result
        except Exception as  e:
            print e
            raise Exception('Error occured in reading Data Structure.\n' + e.message)

    def GetAllMultiAttributeSeries(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making MultiVariableSeries.
        :param selectedResourceType: selected Model name
        :param selectedNetwork: selected Master Network name
        :param selectedScenarior: selected scenario Name
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:

            sql = """
                    SELECT "ObjectTypes"."ObjectType",
                    "Instances"."InstanceName",ScenarioName,"Attributes"."AttributeName" AS MultiAttributeName,"Attributes".AttributeDataTypeCV,
                    SourceName,MethodName,
                    "AttributesColumns"."AttributeName" AS "AttributeName",
                    "AttributesColumns"."AttributeNameCV",
                    "AttributesColumns"."UnitNameCV" AS "AttributeNameUnitName",
                    "ValueOrder","DataValue"
                    FROM ResourceTypes
                    Left JOIN "ObjectTypes"
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
                    -- Join the Mappings to get their DataValuesMappers
                    LEFT JOIN "ValuesMapper"
                    ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID"
                    -- Join the DataValuesMapper to get their MultiAttributeSeries
                    LEFT JOIN "MultiAttributeSeries"
                    ON "MultiAttributeSeries" ."ValuesMapperID"="ValuesMapper"."ValuesMapperID"
                    /*This is an extra join to get to each column name within the MultiColumn Array */
                    -- Join the MultiAttributeSeries to get to their specific DataValuesMapper, now called DataValuesMapperColumn
                    LEFT JOIN "ValuesMapper" As "ValuesMapperColumn"
                    ON "ValuesMapperColumn"."ValuesMapperID"="MultiAttributeSeries"."MappingID_Attribute"
                    -- Join the DataValuesMapperColumn to get back to their specific Mapping, now called MappingColumns
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
                    WHERE
                    "Attributes".AttributeDataTypeCV='MultiAttributeSeries'
                    AND "ResourceTypeAcronym"="{}"
                    AND "MasterNetworkName"= "{}"
                    AND "ScenarioName" ="{}"
                     Order By ScenarioName, AttributeName,ValueOrder asc
                    """.format(selectedResourceType, selectedNetwork, selectedScenarior)

            result = self.session.execute(sql)

            '''Down Table(MultiVariableSeries_table Table) write'''
            complete_result = list()
            strAtrributName = ''
            valueOrder = None
            AttributeName = ''
            tempColumn = {}
            sourceName = ''
            i = 0
            currentrow = 0
            setNumber = 0
            for row in result:
                if row.AttributeName == None or row.AttributeName == "":
                    continue
                if strAtrributName != row.AttributeName:
                    strAtrributName = row.AttributeName
                    tempColumn[row.AttributeName] = []
                    tempColumn[row.AttributeName].append(row.AttributeName)
                    AttributeName = row.AttributeName
                if sourceName != row.ScenarioName:
                    sourceName = row.ScenarioName
                    setNumber = i
                    currentrow = 0
                if AttributeName != row.AttributeName:
                    AttributeName = row.AttributeName
                    currentrow = 0

                if row.AttributeName in tempColumn[row.AttributeName]:
                    index = tempColumn[row.AttributeName].index(row.AttributeName)
                    if index == 0:
                        complete_result.append(
                            [row.ObjectType, row.InstanceName, row.ScenarioName, row.AttributeName,
                             row.SourceName,
                             row.MethodName, row.DataValue])
                        i += 1
                    else:
                        complete_result[setNumber + currentrow].append(row.DataValue)
                        currentrow += 1
                else:
                    currentrow = 0
                    tempColumn[row.AttributeName].append(row.AttributeName)
                    index = tempColumn[row.AttributeName].index(row.AttributeName)
                    if index == 0:
                        complete_result.append(
                            [row.ObjectType, row.InstanceName, row.ScenarioName, row.AttributeName,
                             row.SourceName,
                             row.MethodName, row.DataValue,row.ValueOrder])
                        i += 1
                    else:
                        complete_result[setNumber + currentrow].append(row.DataValue)
                        currentrow += 1

            bottom_table_result = complete_result

            '''Up Table(MultiAttributeName_column Table) write'''
            up_table_column_result = list()
            for key, columnItems in tempColumn.items():
                temList = list()
                temList.append(key)
                for item in columnItems:
                    temList.append(item)
                up_table_column_result.append(temList)
            return up_table_column_result, bottom_table_result

        except Exception as  e:
            print e
            raise Exception('Error occured in reading Data Structure.\n' + e.message)


