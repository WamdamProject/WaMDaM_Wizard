import xlsxwriter
import csv
import os
import xlsxwriter
from collections import OrderedDict
import datetime
# this functon saves all the data into a single excel workbook of multiple sheets

# Excel file name =WEAP_Output
# "C:/Users/Adel/Documents/Results/
# ProvidedDir=self.
# excel_filename = self.excel_filename
# WEAP_Output.xlsx"

# Save the Nodes sheet

def SaveExcel(NodesSheetList, LinksSheetList, result_list, UniqObjectAtt_list,WEAP, excel_filename):
    wb = xlsxwriter.Workbook(excel_filename)
    write_Attributes(UniqObjectAtt_list, wb,WEAP)
    write_nodes(NodesSheetList, wb)
    write_links(LinksSheetList, wb)
    write_Numeric(result_list, wb, WEAP)
    write_Descriptor(result_list, wb, WEAP)
    write_Seasonal(result_list, wb, WEAP)
    write_TimeSeries(result_list, wb)
    write_TimeSeriesValues(result_list, wb, WEAP)
    write_MultiAttributeSeries(result_list, wb, WEAP)

    wb.close()
# print the Nodes into the 3.2_Nodes sheet



def write_Attributes(UniqObjectAtt_list, wb, WEAP):

    AttributeFields = ['ObjectType', 'AttributeName', 'AttributeUnit', 'AttributeDataTypeCV']

    ws = wb.add_worksheet("Attributes")
    row = 0
    col = 0

    for i in range(len(AttributeFields)):
        ws.write(0, i, AttributeFields[i])

    col = 0
    row += 1

    for UniqObjectAtt in UniqObjectAtt_list:
        col = 0
        for key in UniqObjectAtt.keys():
            ws.write(row, col, UniqObjectAtt[key])
            col += 1
        row += 1


def write_nodes(NodesSheetList, wb):
    field_names = ['ObjectType', 'InstanceName', 'InstanceNameCV', 'ScenarioName', 'SourceName', 'MethodName'
        , 'InstanceCategory', 'Longitude_x', 'Latitude_y', 'Description']

    ws = wb.add_worksheet("Nodes")

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

    ws = wb.add_worksheet('Links')

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

    ws = wb.add_worksheet("Numeric")

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




def write_Descriptor(Result_list, wb, WEAP):
    from collections import OrderedDict
    import xlsxwriter

    ws = wb.add_worksheet("FreeText")


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


    ws = wb.add_worksheet("Seasonal")


    SeasonalFields = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName',
                      'SeasonName', 'SeasonNameCV', 'SeasonValue']

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
                    elif month_name == 'Nov':
                        SeasonNameCV = 'November'
                    elif month_name == 'Dec':
                        SeasonNameCV = 'December'
                    elif month_name == 'Jan':
                        SeasonNameCV = 'January'
                    elif month_name == 'Feb':
                        SeasonNameCV = 'February'
                    elif month_name == 'Mar':
                        SeasonNameCV = 'March'
                    elif month_name == 'Apr':
                        SeasonNameCV = 'April'
                    elif month_name == 'May':
                        SeasonNameCV = 'May'
                    elif month_name == 'Jun':
                        SeasonNameCV = 'June'
                    elif month_name == 'Jul':
                        SeasonNameCV = 'July'
                    elif month_name == 'Aug':
                        SeasonNameCV = 'August'
                    elif month_name == 'Sep':
                        SeasonNameCV = 'September'

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

                    col = 0
                    for key in Result.keys():
                        ws.write(row, col, Result[key])
                        col += 1
                    row += 1

                n += 1



def write_TimeSeries(Result_list, wb):

    # Write the 4_TimeSeries table to excel (no data values)
    from collections import OrderedDict
    import xlsxwriter
    import datetime

    Result = {}

    ws = wb.add_worksheet('TimesSeries')

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
        if re['ExpresValueType'] in ['TimeSeries_ExpressValue','TimeSeries']:
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

    ws = wb.add_worksheet('TimeSeriesValues')

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
                    if line_str.strip()[0] in flag_list: continue
                    csv_items.append(line_str)
            else:
                print "Error: the extension, " + file_extension + " is not supported"
                return

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


                # cvsAddress
                col = 0
                row2 += 1
                for key in Resultx.keys():
                    ws.write(row2, col, Resultx[key])
                    col += 1

            n += 1



def write_MultiAttributeSeries(Result_list, wb,WEAP):
    SourceValue = WEAP.ActiveScenario.Name



    Upperfield_names = ['MultiAttributeSeriesName', 'AttributeName1', 'AttributeName2','AttributeName3']

    UpperTable = OrderedDict()


    UpperTable['MultiAttributeSeriesName'] = 'Volume Elevation Curve'

    # WEAP uses the order of Volume, Elevation so we print Volume and its values in the first column
    # and we print Elevation and its values in the second column
    UpperTable['AttributeName1'] = 'Volume-Curve'
    UpperTable['AttributeName2'] = 'Elevation-Curve'


    Lowerfield_names = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName',
                        'MethodName', 'AttributeName1_Values', 'AttributeName2_Values']

    ws = wb.add_worksheet("MultiAttributeSeries")

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


    print 'done saving to excel'



