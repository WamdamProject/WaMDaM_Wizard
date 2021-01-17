import xlsxwriter
import csv
import os
import xlsxwriter
from collections import OrderedDict

import pandas as pd
import datetime
# this functon saves all the data into a single excel workbook of multiple sheets
from pyproj import Proj, transform
# Excel file name =WEAP_Output
# "C:/Users/Adel/Documents/Results/
# ProvidedDir=self.
basic_excel_filename = ''
# WEAP_Output.xlsx"

# Save the Nodes sheet
# BranchesNew_list
def SaveExcel(NodesSheetList, LinksSheetList, result_list, UniqObjectAtt_list,WEAP, excel_filename, Projection_source=''):
    wb = xlsxwriter.Workbook(excel_filename)
    basic_excel_filename = excel_filename
    # write_ResourceTypesObjectTypes(BranchesNew_list, wb,WEAP)
    write_Attributes(UniqObjectAtt_list, wb,WEAP)
    # write_ScenarioNetwork(NodesSheetList, wb)

    if Projection_source:
        SourceSystem = Projection_source

        try:
            OutputSystem = 'EPSG:4326'
            inProj = Proj(init=SourceSystem)
            outProj = Proj(init=OutputSystem)

            for node in range(len(NodesSheetList)):
                x1, y1 = NodesSheetList[node]['Longitude_x'],NodesSheetList[node]['Latitude_y']


                NodesSheetList[node]['Longitude_x'],  NodesSheetList[node]['Latitude_y'] = transform(inProj, outProj, x1, y1)
        except:
            from viewer.Messages_forms.msg_somethigWrong import msg_somethigWrong
            message = msg_somethigWrong(None, msg='The projection code you entered is not correct. Make sure its a valid one')
            message.ShowModal()
            return
    # create xlsx file with "full_path".


    # workbook1 = xlsxwriter.Workbook(full_path)
    # workbook1.add_worksheet('1.1_Organiz&People')
    # workbook1.add_worksheet('1.2_Sources&Methods')
    # workbook1.add_worksheet('2.1_ResourceTypes&ObjectTypes')
    # workbook1.add_worksheet('2.2_Attributes')
    # workbook1.add_worksheet('3.1_Networks&Scenarios')

    try:
        write_MasterNetwork([], wb)
    except Exception, e:
        raise "write_MasterNetworkAndScenario error : " + str(e)

    try:
        write_Scenario([], wb)
    except Exception, e:
        raise "write_Scenario error : " + str(e)

    try:
        write_Organizations([], wb)
    except Exception, e:
        raise "write_Organizations error : " + str(e)

    try:
        write_Peoples([], wb)
    except Exception, e:
        raise "write_Peoples error : " + str(e)

    try:
        write_Sources([], wb)
    except Exception, e:
        raise "write_Sources error : " + str(e)

    try:
        write_Methods([], wb)
    except Exception, e:
        raise "write_Methods error : " + str(e)

    try:
        write_ResourceTypesObjectTypes(NodesSheetList, LinksSheetList, wb)
    except Exception, e:
        raise "write_ResourceTypesObjectTypes error : " + str(e)

    try:
        write_nodes(NodesSheetList, wb)
    except Exception, e:
        raise "write_nodes error : " + str(e)

    print 'done with writing nodes'

    try:
        write_links(LinksSheetList, wb)
    except Exception, e:
        raise "write_links error : " + str(e)
    print 'done with writing links'

    try:
        write_Numeric(result_list, wb, WEAP)
    except Exception, e:
        raise "write_Numeric error : " + str(e)
    print 'done with writing Numeric'

    try:
        write_FreeText(result_list, wb, WEAP)
    except Exception, e:
        raise "write_FreeText error : " + str(e)
    print 'done with writing FreeText'

    try:
        write_Seasonal(result_list, wb, WEAP)
    except Exception, e:
        raise "write_Seasonal error : " + str(e)
    print 'done with writing Seasonal'

    try:
        write_TimeSeries(result_list, wb,WEAP)
    except Exception, e:
        raise "write_TimeSeries error : " + str(e)
    print 'done with writing TimeSeries'

    try:
        write_TimeSeriesValues(result_list, wb, WEAP)
    except Exception, e:
        raise "write_TimeSeriesValues error : " + str(e)
    print 'done with writing TimeSeriesValues'

    try:
        write_MultiAttributeSeries(result_list, wb, WEAP)
    except Exception, e:
        raise "MultiAttributeSeries error : " + str(e)
    print 'done with writing MultiAttributeSeries'

    wb.close()



# here add functions to write to three more sheets

def exportObjecttypes(self, data_result):
    ObjectTypeFields = ['ObjectType', 'ObjectTypology', 'ResourceTypeAcronym', 'ObjectTypeCV', 'Layout',
                        'ObjectCategory', 'Description']

    df = pd.DataFrame(data_result)
    df.to_excel(self.pandas_excel_writer, sheet_name="2.1_ResourceTypes&ObjectTypes", header=True,
                index=False)


# print this one from GetDataStructureFromWeap import ResourceTypes_List
# ResourceTypes_List
# to here exportResourcesType


def exportResourcesType(self, resources_result, objects_result):
    if not resources_result.empty:
        resources_result.to_excel(self.pandas_excel_writer, sheet_name="2.1_ResourceTypes&ObjectTypes", startrow=8,
                                  startcol=0,
                                  header=True,
                                  index=False)
    if not objects_result.empty:
        objects_result.to_excel(self.pandas_excel_writer, sheet_name="2.1_ResourceTypes&ObjectTypes", startrow=16,
                                startcol=0,
                                header=True,
                                index=False)



    People_headers = ["PersonName", "Address", "Email", "Phone", "PersonWebpage", "Position", "OrganizationName"]
    Orgs_header = ["OrganizationName", "OrganizationType", "OrganizationWebpage", "Description"]
    Sources_header = ['SourceName','SourceWebpage','SourceCitation','PersonName','PersonName','Description']
    Methods_header = ['MethodName','MethodWebpage','MethodCitation','MethodTypeCV','PersonName','DataQuality','Description']

# self.write2excel(resources_result, 10, '2.1_ResourceTypes&ObjectTypes')
def exportOrganizations(self, organization_list):
    # df = pd.DataFrame(organization_list)
    organization_list.to_excel(self.pandas_excel_writer, sheet_name="1.1_Organiz&People", startrow=2, startcol=0,
                               header=True,
                               index=False)


# self.write2excel(organization_list, 2, '1.1_Organiz&People')

def exportPeople(self, people_list):
    df = pd.DataFrame(people_list)
    df.to_excel(self.pandas_excel_writer, sheet_name="1.1_Organiz&People", startrow=9, startcol=0, header=True,
                index=False)


# self.write2excel(people_list, 9, '1.1_Organiz&People')

def exportSources(self, source_list):
    # df = pd.DataFrame(source_list)
    source_list.to_excel(self.pandas_excel_writer, sheet_name="1.2_Sources&Methods", startrow=8, startcol=0,
                         header=True,
                         index=False)


# self.write2excel(source_list, 8, '1.2_Sources&Methods')

def exportMethods(self, method_list):
    df = pd.DataFrame(method_list)
    df.to_excel(self.pandas_excel_writer, sheet_name="1.2_Sources&Methods", startrow=19, startcol=0, header=True,
                index=False)


# self.write2excel(method_list, 19, '1.2_Sources&Methods')

def exportMasterNetwork(excel_filename, network_data_result):
    wb = xlsxwriter.Workbook(excel_filename)
    fields = ['MasterNetworkName', 'ResourceTypeAcronym', 'SpatialReferenceNameCV', 'ElevationDatumCV', 'Description']

    ws = wb.add_worksheet("3.1_Networks&Scenarios")
    row = 0
    col = 0

    for i in range(len(fields)):
        ws.write(0, i, fields[i])
    wb.close()

    # network_data_result.to_excel(self.pandas_excel_writer, sheet_name="3.1_Networks&Scenarios", startrow=8, startcol=0,
    #                              header=True,
    #                              index=False)


# scenario_data_result.to_excel(self.pandas_excel_writer, sheet_name="3.1_Networks&Scenarios", startrow=20,
# 							 startcol=1, header=True,
# 							 index=False)
# self.write2excel(network_data_result, 10, '3.1_Networks&Scenarios')

def exportScenario(excel_filename, scenarios_data_result):
    wb = xlsxwriter.Workbook(excel_filename)
    fields = ['MasterNetworkName', 'ResourceTypeAcronym', 'SpatialReferenceNameCV', 'ElevationDatumCV', 'Description']

    ws = wb.add_worksheet("3.1_Networks&Scenarios")
    row = 0
    col = 0

    for i in range(len(fields)):
        ws.write(0, i, fields[i])
    wb.close()

    # df = pd.DataFrame(scenarios_data_result)
    scenarios_data_result.to_excel(self.pandas_excel_writer, sheet_name="3.1_Networks&Scenarios", startrow=18,
                                   startcol=0,
                                   header=True,
                                   index=False)


# self.write2excel(scenarios_data_result, 20, '3.1_Networks&Scenarios')


######################## add the above sheets



# ObjectType	ObjectTypology	DatasetAcronym	ObjectTypeCV	Layout	ObjectCategory	Description








def write_Attributes(UniqObjectAtt_list, wb, WEAP):
    AttributeFields = ['ObjectType', 'AttributeName', 'AttributeName_Abstract', 'AttributeNameCV', 'AttributeUnit',
                       'AttributeUnitCV', 'AttributeDataTypeCV', 'AttributeCategory', 'ModelInputOrOutput',
                       'AttributeDescription','AttributeScale']

    ws = wb.add_worksheet("2.2_Attributes")
    row = 0
    col = 0

    for i in range(len(AttributeFields)):
        ws.write(0, i, AttributeFields[i])

    col = 0
    row += 1

    for UniqObjectAtt in UniqObjectAtt_list:
        col = 0
        for key in AttributeFields:
            try:
                if key == 'AttributeName_Abstract':
                    val = UniqObjectAtt['AttributeName']
                    val = val.split('_')[0]
                else:
                    val = UniqObjectAtt[key]
                ws.write(row, col, val)
            except:
                pass
            col += 1
        row += 1


def write_MasterNetwork(result_list, wb):

    NetworkFieldnames = ['MasterNetworkName', 'ResourceTypeAcronym', 'SpatialReferenceNameCV', 'ElevationDatumCV', 'Description']

    ws = wb.get_worksheet_by_name("3.1_Networks&Scenarios")

    if not ws:
        ws = wb.add_worksheet("3.1_Networks&Scenarios")

    row = 0
    col = 0

    for i in range(len(NetworkFieldnames)):
        ws.write(0, i, NetworkFieldnames[i])


def write_Scenario(result_list, wb):

    ScenarioFieldnames = ['ScenarioName', 'MasterNetworkName', 'SourceName', 'MethodName', 'ScenarioStartDate',
                          'ScenarioEndDate'
        , 'TimeStep', 'TimeStepUnitCV', 'Description']

    ws = wb.get_worksheet_by_name("3.1_Networks&Scenarios")

    if not ws:
        ws = wb.add_worksheet("3.1_Networks&Scenarios")

    row = 0
    col = 0

    for i in range(len(ScenarioFieldnames)):
        ws.write(10, i, ScenarioFieldnames[i])


def write_Organizations(result_list, wb):
    OrganizationsFieldnames = ['MasterNetworkName', 'ResourceTypeAcronym', 'SpatialReferenceNameCV', 'ElevationDatumCV', 'Description']

    ws = wb.get_worksheet_by_name("1.1_Organiz&People")

    if not ws:
        ws = wb.add_worksheet("1.1_Organiz&People")
    row = 0
    col = 0

    for i in range(len(OrganizationsFieldnames)):
        ws.write(2, i, OrganizationsFieldnames[i])

def write_Peoples(result_list, wb):
    PeoplesFieldnames = ['MasterNetworkName', 'ResourceTypeAcronym', 'SpatialReferenceNameCV', 'ElevationDatumCV', 'Description']

    ws = wb.get_worksheet_by_name("1.1_Organiz&People")

    if not ws:
        ws = wb.add_worksheet("1.1_Organiz&People")
    row = 0
    col = 0

    for i in range(len(PeoplesFieldnames)):
        ws.write(9, i, PeoplesFieldnames[i])

def write_Methods(result_list, wb):

    MethodsFieldnames = ['MasterNetworkName', 'ResourceTypeAcronym', 'SpatialReferenceNameCV', 'ElevationDatumCV', 'Description']

    ws = wb.get_worksheet_by_name("1.2_Sources&Methods")

    if not ws:
        ws = wb.add_worksheet("1.2_Sources&Methods")
    row = 0
    col = 0

    for i in range(len(MethodsFieldnames)):
        ws.write(0, i, MethodsFieldnames[i])


def write_Sources(result_list, wb):
    SourcesFieldnames = ['MasterNetworkName', 'ResourceTypeAcronym', 'SpatialReferenceNameCV', 'ElevationDatumCV', 'Description']

    ws = wb.get_worksheet_by_name("1.2_Sources&Methods")

    if not ws:
        ws = wb.add_worksheet("1.2_Sources&Methods")
    row = 0
    col = 0

    for i in range(len(SourcesFieldnames)):
        ws.write(8, i, SourcesFieldnames[i])


def write_ResourceTypesObjectTypes(NodesSheetList, LinksSheetList, wb):
    ResourceTypesObjectTypesFieldnames = ['ObjectType', 'ObjectTypology']

    ws = wb.get_worksheet_by_name("2.1_ResourceTypes&ObjectTypes")

    if not ws:
        ws = wb.add_worksheet("2.1_ResourceTypes&ObjectTypes")
    row = 1
    col = 0

    for i in range(len(ResourceTypesObjectTypesFieldnames)):
        ws.write(0, i, ResourceTypesObjectTypesFieldnames[i])

    data_list = []
    objecttype_list = []
    for nds in NodesSheetList:
        if nds['ObjectType'] in objecttype_list:
            continue
        objecttype_list.append(nds['ObjectType'])

        Nodes = OrderedDict()
        Nodes['ObjectType'] = nds['ObjectType']
        Nodes['ObjectTypology'] = 'Node'
        data_list.append(Nodes)

    objecttype_list = []
    for lks in LinksSheetList:
        if lks['ObjectType'] in objecttype_list:
            continue
        objecttype_list.append(lks['ObjectType'])

        Links = OrderedDict()
        Links['ObjectType'] = lks['ObjectType']
        Links['ObjectTypology'] = 'Link'
        data_list.append(Links)

    # get the unique nodes only [note: a start and end nodes repeate many times]

    for data in data_list:
        col = 0
        for key in data.keys():
            ws.write(row, col, data[key])
            col += 1
        row += 1




def write_nodes(NodesSheetList, wb):
    field_names = ['ObjectType', 'InstanceName', 'InstanceNameCV', 'ScenarioName', 'SourceName', 'MethodName'
        , 'InstanceCategory', 'Longitude_x', 'Latitude_y', 'Description']

    ws = wb.add_worksheet("3.2_Nodes")

    row = 0
    col = 0

    for i in range(len(field_names)):
        ws.write(0, i, field_names[i])

    # print nodes sheet

    col = 0
    row += 1

    descriptionData = []
    Nodes_list=[]

    for nds in NodesSheetList:
        Nodes = OrderedDict()
        Nodes['ObjectType'] = nds['ObjectType']
        Nodes['InstanceName'] = nds['InstanceName']
        Nodes['InstanceNameCV'] = nds['InstanceNameCV']
        Nodes['ScenarioName'] = nds['ScenarioName']
        Nodes['SourceName'] = nds['SourceName']
        Nodes['MethodName'] = nds['MethodName']
        Nodes['InstanceCategory'] = nds['InstanceCategory']
        Nodes['Longitude_x'] = nds['Longitude_x']
        Nodes['Latitude_y'] = nds['Latitude_y']
        Nodes['Description'] = nds['Description']
        Nodes_list.append(Nodes)

    # get the unique nodes only [note: a start and end nodes repeate many times]

    for nodesSheet in Nodes_list:
        col = 0
        if not nodesSheet['Description'] in descriptionData:
            descriptionData.append(nodesSheet['Description'])
            for key in nodesSheet.keys():
                ws.write(row, col, nodesSheet[key])
                col += 1
            row += 1





# Save the links sheet
# print the Links into the 3.3_Links sheet
# import xlsxwriter

# dont print the BranchName
def write_links(LinksSheetList, wb):

    field_names = ['ObjectType', 'InstanceName', 'InstanceNameCV', 'ScenarioName', 'SourceName', 'MethodName'
        , 'StartNodeInstanceName', 'EndNodeInstanceName', 'InstanceCategory', 'Description']

    ws = wb.add_worksheet('3.3_Links')

    row = 0
    col = 0

    for i in range(len(field_names)):
        ws.write(0, i, field_names[i])

    col = 0
    row += 1
    # print LinksSheet

    descriptionLinksData = []
    Links_list=[]

    for lks in LinksSheetList:
        Links = OrderedDict()
        Links['ObjectType'] = lks['ObjectType']
        Links['InstanceName'] = lks['InstanceName']
        Links['InstanceNameCV'] = lks['InstanceNameCV']
        Links['ScenarioName'] = lks['ScenarioName']
        Links['SourceName'] = lks['SourceName']
        Links['MethodName'] = lks['MethodName']
        Links['StartNodeInstanceName'] = lks['StartNodeInstanceName']
        Links['EndNodeInstanceName'] = lks['EndNodeInstanceName']
        Links['InstanceCategory'] = lks['InstanceCategory']
        Links['Description'] = lks['Description']
        Links_list.append(Links)

    # get the unique links only

    for linksSheet in Links_list:
        col = 0
        if not linksSheet['Description'] in descriptionLinksData:
            descriptionLinksData.append(linksSheet['Description'])
            for key in linksSheet.keys():
                ws.write(row, col, linksSheet[key])
                col += 1
            row += 1

    # wb.close()

    print 'link done'

# Save the TimeSeries


def write_Numeric(Result_list, wb, WEAP):

    ws = wb.add_worksheet("4_NumericValues")

    NumeircFields = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName',
                     'NumericValue']

    for i in range(len(NumeircFields)):
        ws.write(0, i, NumeircFields[i])

    row = 1

    for re in Result_list:

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

            col = 0
            for key in Result.keys():
                ws.write(row, col, Result[key])
                col += 1
            row += 1




def write_FreeText(Result_list, wb, WEAP):
    from collections import OrderedDict
    import xlsxwriter

    ws = wb.add_worksheet("4_FreeText")


    FreeTextFields = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName', 'FreeText']

    for i in range(len(FreeTextFields)):
        ws.write(0, i, FreeTextFields[i])

    row = 1

    for re in Result_list:

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
            Result['FreeText_ExpressValue'] = re['ExpresValue']

            col = 0
            for key in Result.keys():
                ws.write(row, col, Result[key])
                col += 1
            row += 1
# close ()

def write_Seasonal(Result_list, wb, WEAP):

    # Seasonal_ExpressValue
    #     if re['ExpresValueType'] == 'Seasonal_ExpressValue':


    ws = wb.add_worksheet("4_SeasonalNumericValues")


    SeasonalFields = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName',
                      'SeasonName', 'SeasonNameCV', 'SeasonValue','SeasonDateFormate']

    for i in range(len(SeasonalFields)):
        ws.write(0, i, SeasonalFields[i])

    row = 1

    for re in Result_list:

        if re['ExpresValueType'] in ['Seasonal_ExpressValue','SeasonalNumericValues']:

            ExpresValue1 = re['ExpresValue'].split('MonthlyValues(')[-1].split(')')[0].split(',')
            #         print ExpresValue1

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
                    Result['SeasonValue'] = SeasonValue
                    Result['SeasonDateFormate'] = SeasonDateFormate

                    col = 0
                    for key in Result.keys():
                        ws.write(row, col, Result[key])
                        col += 1
                    row += 1

                n += 1



def write_TimeSeries(Result_list, wb,WEAP):

    # Write the 4_TimeSeries table to excel (no data values)
    from collections import OrderedDict
    import xlsxwriter
    import datetime

    Result = {}

    ws = wb.add_worksheet('4_TimeSeries')

    field_names = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName', 'YearType',
                   'AggregationStatisticCV',
                   'AggregationInterval', 'IntervalTimeUnit', 'IsRegular', 'NoDataValue', 'Description']

    for i in range(len(field_names)):
        ws.write(0, i, field_names[i])

    row = 0
    col = 0

    n = 0
    for re in Result_list:
        # In Result_list, TimeSeries_ExpressValue
        if re['ExpresValueType'] in ['TimeSeries_ExpressValue']:

           #-----------------------------------------------------------------------------------------------------
           # if path to the CSV or text file is invalid (no data inside the path), then skip this time series.
           # if we get a time series record in this sheet and we dont get it in the values sheet, then we end up
           # with an extra metadata time series that has no values in WaMDaM.
           # thats ok generally, but it causes issues when we upload WaMdaM data into OpenAgua and download it back

           # Read the csv file within the name inside ExpresValue

           ActiveArea = WEAP.ActiveArea.Name
           Scenario = WEAP.ActiveScenario.Name

           WEAPAreasDirectory = WEAP.AreasDirectory

           # print WEAPAreasDirectory

           CsvFilePath = WEAPAreasDirectory + ActiveArea + "/"
           # print CsvFilePath
           csv_all_data_list = []
           n = 0
           # http: // www.weap21.org / WebHelp / Read_From_File.htm
           # check if it is csv or txt
           Fileformat = []

           # if xx==.txt or .TXT
           #     yy=.csv or .CSV
           #
           '''skip reading the lines if they start with[';','$', '#']'''

           filename, file_extension = os.path.splitext(
               re['ExpresValue'].split('ReadFromFile(')[-1].replace(')', ''))

           csv_file_name = re['ExpresValue'].split('ReadFromFile(')[-1]

           if csv_file_name[0] == '.':
               csv_file_name = csv_file_name[1:]

           if csv_file_name[0] == "\\":
               csv_file_name = csv_file_name.replace('\\', "/")[1:]

           if ')' in csv_file_name:
               csv_file_name = csv_file_name.replace(')', '')

           if "\\" in CsvFilePath:
               CsvFilePath = CsvFilePath.replace('\\', '/')[1:]

               CsvFilePath = 'C' + CsvFilePath

           #
           if ',' in csv_file_name:
               temp_name = csv_file_name.split(',')[0]
               filename, file_extension = os.path.splitext(temp_name)
               if filename and file_extension.lower() == '.csv':
                   csv_file_name = temp_name
           # csv_file_full_path = CsvFilePath + csv_file_name

           if CsvFilePath not in csv_file_name.replace('\\', '/'):
               csv_file_full_path = CsvFilePath + csv_file_name
           else:
               csv_file_full_path = csv_file_name

           if not os.path.isfile(csv_file_full_path):
               continue
           #-----------------------------------------------------------------------------------------------------
           BranchType = re['BranchType']
           InstanceName = re['InstanceName']
           VariableName = re['VariableName']
           OriginalBranchName = re['BranchName']
           CSV_Address = re['ExpresValue']
           Result = OrderedDict()
           Result['ObjectType'] = BranchType
           Result['InstanceName'] = InstanceName
           Result['ScenarioName'] = ''
           Result['AttributeName'] = VariableName
           Result['SourceName'] = ''
           Result['MethodName'] = ''
           Result['YearType'] = 'CalenderYear'
           if BranchType == 'Demand Site':
               Result['AggregationStatisticCV'] = 'Cumulative'
           else:
               Result['AggregationStatisticCV'] = 'Average'
           Result['AggregationInterval'] = 1
           Result['IntervalTimeUnit'] = 'month'
           Result['IsRegular'] = ''
           Result['NoDataValue'] = '-9999'
           Result['Description'] = CSV_Address

           col = 0
           row += 1
           for key in Result.keys():
               if key == "BranchName": continue
               ws.write(row, col, Result[key])
               col += 1
        n += 1
        # print 'time series done'


def write_TimeSeriesValues(Result_list, wb,WEAP):

    ws = wb.add_worksheet('4_TimeSeriesValues')

    field_names = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'DateTimeStamp', 'DataValue',
                   'cvsAddress']
    for i in range(len(field_names)):
        ws.write(0, i, field_names[i])

    # print csv_all_data_list[0]

    row2 = 0
    col = 0

    # Read the csv file within the name inside ExpresValue

    ActiveArea = WEAP.ActiveArea.Name
    Scenario = WEAP.ActiveScenario.Name

    WEAPAreasDirectory = WEAP.AreasDirectory

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
    # try:
    for re in Result_list:
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
            # csv_file_full_path = CsvFilePath + csv_file_name
            if CsvFilePath not in csv_file_name.replace('\\', '/'):
                csv_file_full_path = CsvFilePath + csv_file_name
            else:
                csv_file_full_path = csv_file_name

            if not os.path.isfile(csv_file_full_path):
                continue
            #     if csv_file_full_path=="C:\Users\Adel\Documents\WEAP Areas\BearRiverFeb2017_V10.9/..\BearRiverFeb2017_V10.7\Reach_gains\flow_above_alexander_gain_weap_pos.csv":
            f = open(csv_file_full_path)

            flag_list = [';', '$', '#']

            if file_extension.lower() == '.csv':
                csv_items_temp = csv.reader(f)
                csv_items = []
                for line_str in csv_items_temp:
                    if len(line_str) == 0:
                        continue
                    if len(line_str[0].strip()) == 0:
                        continue

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
                return

            csv_data_list = []

            for i, row in enumerate(csv_items):
                # if not row.strip():
                if row[0].strip() and row[1].strip():
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
                print BranchTypex,BranchName,VariableName
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


                # cvsAddress
                col = 0
                row2 += 1
                for key in Resultx.keys():
                    ws.write(row2, col, Resultx[key])
                    col += 1

            n += 1
    # except:
    #     pass



def write_MultiAttributeSeries(Result_list, wb,WEAP):
    SourceValue = WEAP.ActiveScenario.Name



    Upperfield_names = ['MultiAttributeSeriesName', 'AttributeName1', 'AttributeName2','AttributeName3']

    UpperTable = OrderedDict()


    UpperTable['MultiAttributeSeriesName'] = 'Volume Elevation Curve_MA'

    # WEAP uses the order of Volume, Elevation so we print Volume and its values in the first column
    # and we print Elevation and its values in the second column
    UpperTable['AttributeName1'] = 'Volume-Curve'
    UpperTable['AttributeName2'] = 'Elevation-Curve'


    Lowerfield_names = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName',
                        'MethodName', 'AttributeName1_Values', 'AttributeName2_Values']

    ws = wb.add_worksheet("4_MultiAttributeSeries")

    for i, column_val in enumerate(Upperfield_names):
        # if i <4: continue
        ws.write(0, i+5, column_val)

    row = 1
    col = 5

    for key in UpperTable.keys():
        ws.write(row, col, UpperTable[key])
        col += 1
    row += 1

    # n += 1



    for i in range(len(Lowerfield_names)):
        ws.write(9, i, Lowerfield_names[i])

    row = 10
    col = 0
    # print Result_list
    for re in Result_list:

        if re['ExpresValueType'] == 'MultiColumns_ExpressValue':

            ExpresValue1 = re['ExpresValue'].split('VolumeElevation(')[-1].split(')')[0].split(',')
            #         print ExpresValue1

            data_pair = []

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

                    col = 0
                    for key in LowerTable.keys():
                        ws.write(row, col, LowerTable[key])
                        col += 1
                    row += 1

                n += 1


    print 'Done saving WEAP network and its data into A WaMDaM Excel Template'



