

from GetValues import GetValues_WEAP
from Extract_Network import Extract_Network

from collections import OrderedDict
import os, csv
'''
    This class is used to get result that query to get data of values in sqlite db.
'''

class GetValuesAllFromWeap(object):
    def __init__(self, weap):
        self.WEAP = weap
        self.NodesSheetList, self.LinksSheetList, self.unique_object_types_value_list,self.BranchesNew_list = Extract_Network(self.WEAP)
        self.result_list, self.uniqObjectAtt_list = GetValues_WEAP(self.WEAP, self.BranchesNew_list, self.unique_object_types_value_list)

    def getNumericValue(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making NumericValues_table.
        :param selectedType: selected Model Type
        :param selectedAttribute: controlled dNetwork
        :param selectedInstance: controlled Scenarior
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:
            complete_result = list()
            for re in self.result_list:
                if re['ExpresValueType'] in ['Numeric_ExpressValue','NumericValues']:
                    BranchType = re['BranchType']
                    InstanceName = re['InstanceName']
                    VariableName = re['VariableName']

                    Result = OrderedDict()
                    Result['ObjectType'] = BranchType
                    Result['InstanceName'] = InstanceName
                    Result['ScenarioName'] = ''
                    Result['AttributeName'] = VariableName
                    Result['SourceName'] = ''
                    Result['MethodName'] = ''
                    Result['NumericValue'] = re['ExpresValue']

                    complete_result.append(Result.values())
            return complete_result
        except Exception as  e:
            print e
            raise Exception('Erro occure in reading Data Structure.\n' + e.message)

    def getFreeText(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making FreeTextSheet.
        :param selectedType: selected Model Type
        :param selectedAttribute: controlled Network
        :param selectedInstance: controlled Scenarior
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:
            complete_result = list()
            for re in self.result_list:
                if re['ExpresValueType'] == 'FreeText':
                    BranchType = re['BranchType']
                    InstanceName = re['InstanceName']
                    VariableName = re['VariableName']

                    Result = OrderedDict()
                    Result['ObjectType'] = BranchType
                    Result['InstanceName'] = InstanceName
                    Result['ScenarioName'] = ''
                    Result['AttributeName'] = VariableName
                    Result['SourceName'] = ''
                    Result['MethodName'] = ''
                    Result['FreeTextValue'] = re['ExpresValue']

                    complete_result.append(Result.values())
            return complete_result
        except Exception as  e:
            print e
            raise Exception('Erro occure in reading Data Structure.\n' + e.message)
    #
    def getSeasonaNumericValues(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making SeasonalParameter.
        :param selectedResourceType: selected Model name
        :param selectedNetwork: selected Master Network name
        :param selectedScenarior: selected scenario Name
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:
            complete_result = list()
            for re in self.result_list:
                if re['ExpresValueType'] in ['Seasonal_ExpressValue','SeasonalNumericValues']:

                    ExpresValue1 = re['ExpresValue'].split('MonthlyValues(')[-1].split(')')[0].split(',')
                    data_pair = []

                    BranchType = re['BranchType']
                    InstanceName = re['InstanceName']
                    VariableName = re['VariableName']
                    SeasonNameCV=''
                    SeasonDateFormate=''

                    n = 1
                    for e in ExpresValue1:
                        # It means the remainder of dividing by 2. Because always first value is AttributeName1_Values and  second value is AttributeName2_Values.
                        if n % 2 == 0:
                            month_name = ExpresValue1[n - 2]
                            #strip empty space before or after the text value in month_name
                            month_name=month_name.strip()
                            # add controlled vocabulary to each season shortcut name used in WEAP
                            if month_name == 'Oct':
                                SeasonNameCV='October'
                                SeasonDateFormate='1999/10/1'

                            elif month_name == 'Nov':
                                SeasonNameCV = 'November'
                                SeasonDateFormate='1999/11/1'

                            elif month_name == 'Dec':
                                SeasonNameCV = 'December'
                                SeasonDateFormate='1999/12/1'
                            elif month_name == 'Jan':
                                SeasonNameCV = 'January'
                                SeasonDateFormate='1999/01/1'

                            elif month_name == 'Feb':
                                SeasonNameCV = 'February'
                                SeasonDateFormate='1999/02/1'

                            elif month_name == 'Mar':
                                SeasonNameCV = 'March'
                                SeasonDateFormate='1999/03/1'

                            elif month_name == 'Apr':
                                SeasonNameCV = 'April'
                                SeasonDateFormate='1999/04/1'

                            elif month_name == 'May':
                                SeasonNameCV = 'May'
                                SeasonDateFormate='1999/05/1'

                            elif month_name == 'Jun':
                                SeasonNameCV = 'June'
                                SeasonDateFormate='1999/06/1'


                            elif month_name == 'Jul':
                                SeasonNameCV = 'July'
                                SeasonDateFormate='1999/07/1'

                            elif month_name == 'Aug':
                                SeasonNameCV = 'August'
                                SeasonDateFormate='1999/08/1'

                            elif month_name == 'Sep':
                                SeasonNameCV = 'September'
                                SeasonDateFormate='1999/09/1'

                            SeasonValue = ExpresValue1[n - 1]
                            #                 print month_name, value

                            Result = OrderedDict()
                            Result['ObjectType'] = BranchType
                            Result['InstanceName'] = InstanceName
                            Result['ScenarioName'] = ''
                            Result['AttributeName'] = VariableName
                            Result['SourceName'] = ''
                            Result['MethodName'] = ''
                            Result['SeasonName'] = month_name
                            Result['SeasonNameCV'] = SeasonNameCV
                            Result['SeasonNumericValue'] = SeasonValue
                            Result['SeasonDateFormate'] = SeasonDateFormate
                            complete_result.append(Result.values())
            return complete_result
        except Exception as  e:
            print e
            raise Exception('Erro occure in reading Data Structure.\n' + e.message)
    #
    def gettTimeSeriesValues(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making TimeSeries.
        :param selectedResourceType: selected Model name
        :param selectedNetwork: selected Master Network name
        :param selectedScenarior: selected scenario Name
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:
            field_names = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'DateTimeStamp', 'DataValue',
                           'cvsAddress']

            ActiveArea = self.WEAP.ActiveArea.Name
            Scenario = self.WEAP.ActiveScenario.Name

            WEAPAreasDirectory = self.WEAP.AreasDirectory

            # print WEAPAreasDirectory

            CsvFilePath = WEAPAreasDirectory + ActiveArea + "/"
            # print CsvFilePath
            csv_all_data_list = []
            n = 0
            # http: // www.weap21.org / WebHelp / Read_From_File.htm
            #check if it is csv or txt
            Fileformat=[]

            # if xx==.txt or .TXT
            #     yy=.csv or .CSV
            #
            '''skip reading the lines if they start with[';','$', '#']'''

            complete_result = list()

            for re in self.result_list:
                if re['ExpresValueType'] == 'TimeSeries_ExpressValue':
                    filename, file_extension = os.path.splitext(re['ExpresValue'].split('ReadFromFile(')[-1].replace(')', ''))

                    csv_file_name = re['ExpresValue'].split('ReadFromFile(')[-1]

                    if csv_file_name[0] == '.':
                        csv_file_name  = csv_file_name[1:]

                    if csv_file_name[0] == "\\":
                        csv_file_name = csv_file_name.replace('\\', '/')[1:]

                    if ')' in csv_file_name:
                        csv_file_name=csv_file_name.replace(')', '')

                    if "\\" in CsvFilePath:
                        CsvFilePath = CsvFilePath.replace('\\', '/')[1:]

                        CsvFilePath='C'+CsvFilePath

                    #
                    if ',' in csv_file_name:
                        temp_name = csv_file_name.split(',')[0]
                        filename, file_extension = os.path.splitext(temp_name)
                        if filename and file_extension.lower() == '.csv':
                            csv_file_name = temp_name
                    csv_file_full_path = CsvFilePath + csv_file_name
                    if not os.path.isfile(csv_file_full_path):
                        continue
                    #     if csv_file_full_path=="C:\Users\Adel\Documents\WEAP Areas\BearRiverFeb2017_V10.9/..\BearRiverFeb2017_V10.7\Reach_gains\flow_above_alexander_gain_weap_pos.csv":
                    f = open(csv_file_full_path)

                    flag_list = [';', '$', '#']

                    if file_extension.lower() == '.csv':
                        csv_items_temp = csv.reader(f)
                        csv_items = []
                        for line_str in csv_items_temp:
                            if line_str[0].strip()[0] in flag_list: continue
                            csv_items.append(line_str)
                    elif file_extension.lower() == '.txt':
                        csv_items_temp = f.readlines()
                        csv_items = []
                        for line_str in csv_items_temp:
                            datas = line_str.split(',')
                            if datas[0].strip()[0] in flag_list: continue
                            csv_items.append(datas)
                    else:
                        print "Error: the extension, " + file_extension + " is not supported"
                        return []

                    csv_data_list = []

                    for i, row in enumerate(csv_items):
                        a_data = row[0] # year
                        b_data = row[1] # Month
                        c_data = row[2] # Value

                        csv_data_list.append([a_data, b_data, c_data])
                    csv_all_data_list.append(csv_data_list)
                            # In Result_list, TimeSeries_ExpressValue
                    BranchTypex = re['BranchType']
                    BranchName = re['InstanceName']
                    VariableName = re['VariableName']
                    #         print BranchTypex
                    #         print BranchName
                    #         print VariableName
                    for csv_data in csv_all_data_list[n]:
                        Resultx = OrderedDict()

                        Resultx['ObjectType'] = BranchTypex
                        Resultx['InstanceName'] = BranchName
                        Resultx['ScenarioName'] = ''
                        Resultx['AttributeName'] = VariableName
                        #             print csv_data
                        # This one is a combination of  a_data = row[0] and  b_data = row[1] and the first day of the month [day/month/1996] =1/1/1996
                        Resultx['DateTimeStamp'] = '{}/1/{}'.format(csv_data[1], csv_data[0])
                        DataValue = csv_data[2]
                        if DataValue == 'NA':
                            DataValue = '-9999'
                        Resultx['DataValue'] = DataValue
                        #         Result_list.append(Resultx)
                        complete_result.append(Resultx.values())
            return complete_result
        except Exception as  e:
            print e
            raise Exception('Error occured in reading Data Structure.\n' + e.message)



    def getMultiAttributeSeries(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
        '''
        This method is used to get data making MultiVariableSeries.
        :param selectedResourceType: selected Model name
        :param selectedNetwork: selected Master Network name
        :param selectedScenarior: selected scenario Name
        :param excelPath: full path of excel file to export data
        :return: None
        '''
        try:
            up_table_column_result = list()
            bottom_table_result = list()
            SourceValue = self.WEAP.ActiveScenario.Name

            UpperTable = OrderedDict()
            UpperTable['MultiAttributeSeriesName'] = 'Volume Elevation Curve'
            # WEAP uses the order of Volume, Elevation so we print Volume and its values in the first column
            # and we print Elevation and its values in the second column
            UpperTable['AttributeName1'] = 'Volume-Curve'
            UpperTable['AttributeName2'] = 'Elevation-Curve'
            up_table_column_result.append(UpperTable.values())

            # print Result_list
            for re in self.result_list:
                if re['ExpresValueType'] == 'MultiColumns_ExpressValue':
                    ExpresValue1 = re['ExpresValue'].split('VolumeElevation(')[-1].split(')')[0].split(',')
                    #         print ExpresValue1
                    n = 1
                    for e in ExpresValue1:
                        # It means the remainder of dividing by 2. Because always first value is AttributeName1_Values and  second value is AttributeName2_Values.
                        if n % 2 == 0:
                            #             data_pair.append([ExpresValue1[n-2], ExpresValue1[n-1]])

                            #     print data_pair

                            # # create two vectors
                            # first_data = ExpresValue['Value'][j]
                            # second_data = ExpresValue['Value'][j + n]
                            LowerTable = OrderedDict()

                            LowerTable['ObjectType'] = re['BranchType']
                            LowerTable['InstanceName'] = re['InstanceName']
                            LowerTable['ScenarioName'] = SourceValue
                            LowerTable['AttributeName'] = re['VariableName']
                            LowerTable['SourceName'] = SourceValue
                            LowerTable['MethodName'] = 'Water Evaluation And Planning System'
                            LowerTable['AttributeName1_Values'] = ExpresValue1[n - 2]
                            LowerTable['AttributeName2_Values'] = ExpresValue1[n - 1]

                            bottom_table_result.append(LowerTable.values())

            return up_table_column_result, bottom_table_result

        except Exception as  e:
            print e
            raise Exception('Error occured in reading Data Structure.\n' + e.message)


    # def getTextConrolledValues(self, selectedResourceType='', selectedNetwork='', selectedScenarior=''):
    #     '''
    #     This method is used to get data making CategoricalValues_table.
    #     :param selectedResourceType: selected Model name
    #     :param selectedNetwork: selected Master Network name
    #     :param selectedScenarior: selected scenario Name
    #     :param excelPath: full path of excel file to export data
    #     :return: None
    #     '''
    #     try:
    #         if selectedResourceType == '' and selectedNetwork == '' and selectedScenarior == '':
    #             sql = 'SELECT Attributes.AttributeName, ObjectType, SourceName, InstanceName,MasterNetworkName,' \
    #                   'ScenarioName,MethodName,CategoricalValueCV ' \
    #                 'FROM "ResourceTypes" '\
    #                 'Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" '\
    #                 'Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" '\
    #                 'Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" '\
    #                 'Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" '\
    #                 'Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" '\
    #                 'Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" '\
    #                 'Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" '\
    #                 'Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" '\
    #                 'Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" '\
    #                 'Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" '\
    #                 'LEFT JOIN "CategoricalValues" ON "CategoricalValues"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" '\
    #                 'LEFT JOIN "CV_Categorical" ON "CV_Categorical"."Name"= "CategoricalValues"."CategoricalValueCV" '\
    #                 'WHERE "Attributes"."AttributeDataTypeCV"="CategoricalValues"'
    #         else:
    #             sql = 'SELECT Attributes.AttributeName, ObjectType, SourceName, InstanceName,MasterNetworkName,' \
    #                   'ScenarioName,MethodName,CategoricalValueCV ' \
    #                 'FROM "ResourceTypes" '\
    #                 'Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" '\
    #                 'Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" '\
    #                 'Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" '\
    #                 'Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" '\
    #                 'Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" '\
    #                 'Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" '\
    #                 'Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" '\
    #                 'Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" '\
    #                 'Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" '\
    #                 'Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" '\
    #                 'LEFT JOIN "CategoricalValues" ON "CategoricalValues"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" '\
    #                 'LEFT JOIN "CV_Categorical" ON "CV_Categorical"."Name"= "CategoricalValues"."CategoricalValueCV" '\
    #                 'WHERE "Attributes"."AttributeDataTypeCV"="CategoricalValues" AND "ResourceTypes"."ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"'\
    #                 .format(selectedResourceType, selectedNetwork, selectedScenarior)
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
    #                                     row.CategoricalValueCV])
    #         return complete_result
    #     except Exception as  e:
    #         raise Exception('Error occured in reading Data Structure.\n' + e.message)
    #
    # def getElectronicFilesValues(self, selectedResourceType='', selectedNetwork='', selectedScenarior='', excelPath=''):
    #     '''
    #     This method is used to get data making ElectronicFiles.
    #     :param selectedResourceType: selected Model name
    #     :param selectedNetwork: selected Master Network name
    #     :param selectedScenarior: selected scenario Name
    #     :param excelPath: full path of excel file to export data
    #     :return: None
    #     '''
    #     try:
    #         if selectedResourceType =='' and selectedNetwork == '' and selectedScenarior == '':
    #             sql = 'SELECT ObjectType, AttributeName, SourceName, InstanceName,MasterNetworkName,' \
    #                   'ScenarioName,MethodName,FileName, ElectronicFileFormatCV, "File"."Description" ' \
    #                 'FROM "ResourceTypes" '\
    #                 'Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" '\
    #                 'Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" '\
    #                 'Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" '\
    #                 'Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" '\
    #                 'Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" '\
    #                 'Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" '\
    #                 'Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" '\
    #                 'Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" '\
    #                 'Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" '\
    #                 'Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" '\
    #                 'LEFT JOIN "Files" ON "File"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" '\
    #                 'Left JOIN "CV_ElectronicFormat" ON "CV_ElectronicFormat"."Name"="File"."ElectronicFileFormatCV" '\
    #                 'WHERE "Attributes"."AttributeDataTypeCV"="File"'
    #         else:
    #             sql = 'SELECT ObjectType, AttributeName, SourceName, InstanceName,MasterNetworkName,' \
    #                   'ScenarioName,MethodName,FileName, ElectronicFileFormatCV, "File"."Description" ' \
    #                 'FROM "ResourceTypes" '\
    #                 'Left JOIN "ObjectTypes" ON "ObjectTypes"."ResourceTypeID"="ResourceTypes"."ResourceTypeID" '\
    #                 'Left JOIN "Attributes" ON "Attributes"."ObjectTypeID"="ObjectTypes"."ObjectTypeID" '\
    #                 'Left JOIN "Mappings" ON "Mappings"."AttributeID"= "Attributes"."AttributeID" '\
    #                 'Left JOIN "ValuesMapper" ON "ValuesMapper"."ValuesMapperID"="Mappings"."ValuesMapperID" '\
    #                 'Left JOIN "ScenarioMappings" ON "ScenarioMappings"."MappingID"="Mappings"."MappingID" '\
    #                 'Left JOIN "Scenarios" ON "Scenarios"."ScenarioID"="ScenarioMappings"."ScenarioID" '\
    #                 'Left JOIN "MasterNetworks" ON "MasterNetworks"."MasterNetworkID"="Scenarios"."MasterNetworkID" '\
    #                 'Left JOIN "Methods" ON "Methods"."MethodID"="Mappings"."MethodID" '\
    #                 'Left JOIN "Sources" ON "Sources"."SourceID"="Mappings"."SourceID" '\
    #                 'Left JOIN "Instances" ON "Instances"."InstanceID"="Mappings"."InstanceID" '\
    #                 'LEFT JOIN "Files" ON "File"."ValuesMapperID" = "ValuesMapper"."ValuesMapperID" '\
    #                 'Left JOIN "CV_ElectronicFileFormat" ON "CV_ElectronicFormat"."Name"="File"."ElectronicFileFormatCV" '\
    #                 'WHERE "Attributes"."AttributeDataTypeCV"="File" AND "ResourceTypes"."ResourceTypeAcronym" = "{}" AND "MasterNetworkName" = "{}" AND "ScenarioName" = "{}"'\
    #                 .format(selectedResourceType, selectedNetwork, selectedScenarior)
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
    #                                     row.FileName, row.ElectronicFileFormatCV, excelPath, row.Description])
    #
    #         return complete_result
    #     except Exception as  e:
    #         return []