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



def SaveExcel(df_all, excel_filename):
    wb = xlsxwriter.Workbook(excel_filename)
    # write_Attributes(UniqObjectAtt_list, wb,WEAP)
    Nodes_list = write_nodes(df_all, wb)
    Links_list = write_links(df_all, wb)
    write_Numeric(df_all, wb,  Nodes_list, Links_list)
    write_Descriptor(df_all, wb,  Nodes_list, Links_list)
    write_Seasonal(df_all, wb, Nodes_list, Links_list)
    # write_TimeSeries(result_list, wb)
    # write_TimeSeriesValues(result_list, wb, WEAP)
    write_MultiAttributeSeries(df_all, wb, Nodes_list, Links_list)

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


def write_nodes(df_all, wb):
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

    # for symbol, df in df_all.items():
    for symbol_name, df in df_all.items():
        if symbol_name in ['dem', 'v','j']:
            for instance_name in  df['*']:

                Nodes = OrderedDict()
                Nodes['ObjectType'] = symbol_name
                Nodes['InstanceName'] =  instance_name
                Nodes['InstanceNameCV'] = ''
                Nodes['ScenarioName'] = ''
                Nodes['SourceName'] = ''
                Nodes['MethodName'] = ''
                Nodes['InstanceCategory'] = ''
                Nodes['Longitude_x'] = ''
                Nodes['Latitude_y'] = ''
                Nodes['Description'] = ''
                Nodes_list.append(Nodes)

    # get the unique nodes only [note: a start and end nodes repeate many times]

    for nodesSheet in Nodes_list:
        col = 0
        for key in nodesSheet.keys():
            ws.write(row, col, nodesSheet[key])
            col += 1
        row += 1



    return Nodes_list
# Save the links sheet
# print the Links into the 3.3_Links sheet
# import xlsxwriter

# dont print the BranchName
def write_links(df_all, wb):

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

    for symbol_name, df in df_all.items():
        if symbol_name in ['envSiteExist','returnFlowExist','DiversionExist']:
            for i, itmes in df.iterrows():

                Links = OrderedDict()
                Links['ObjectType'] = symbol_name
                Links['InstanceName'] = itmes[0]+itmes[1] #concatnate both first and second columnbs
                Links['InstanceNameCV'] = ''
                Links['ScenarioName'] = ''
                Links['SourceName'] =''
                Links['MethodName'] = ''
                Links['StartNodeInstanceName'] = itmes[0] # first column
                Links['EndNodeInstanceName'] = itmes[1] # second column
                Links['InstanceCategory'] = ''
                Links['Description'] = ''
                Links_list.append(Links)

    # get the unique links only

    for linksSheet in Links_list:
        col = 0
        for key in linksSheet.keys():
            ws.write(row, col, linksSheet[key])
            col += 1
        row += 1

    # wb.close()

    print 'link done'
    return Links_list

# Save the TimeSeries


def write_Numeric(df_all, wb, Links_list,Nodes_list):

    ws = wb.add_worksheet("Numeric")

    NumeircFields = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName',
                     'NumericValue']

    for i in range(len(NumeircFields)):
        ws.write(0, i, NumeircFields[i])

    row = 1

    # for df in df_all:

    Numeric_list = []

    list1 = []

    for node in Nodes_list:
        list1.append({'InstanceName': node['InstanceName'], 'ObjectType': node['ObjectType']})
    for node in Links_list:
        list1.append({'InstanceName': node['InstanceName'], 'ObjectType': node['ObjectType']})

    for symbol_name, df in df_all.items():
        if symbol_name in ['InitD','InitSTOR','b','CMax','cst','dCap','DValue','lng','maxstore','minstore']:  #'QLoop' dReqBase,'evap'
            for i, itmes in df.iterrows():
                Instance_name = itmes[0]
                if len(itmes) > 2:
                    Instance_name = itmes[0] + itmes[1]
                ObjectType = ''
                # append them together to be one new list
                for instance_name_item in list1:
                    # look up the Object Type based on the given Instance name
                    if Instance_name == instance_name_item['InstanceName']:
                        ObjectType = instance_name_item['ObjectType']
                        break

                Numeric = OrderedDict()
                Numeric['ObjectType'] = ObjectType
                if ObjectType !='':
                    Numeric['InstanceName'] = Instance_name
                    Numeric['ScenarioName'] = ''
                    Numeric['AttributeName'] = symbol_name
                    Numeric['SourceName'] = ''
                    Numeric['MethodName'] = ''
                    Numeric['NumericValue'] = itmes[len(itmes)-1]

                    Numeric_list.append(Numeric)

    for Numeric_sheet in Numeric_list:
        col = 0
        for key in Numeric_sheet.keys():
            ws.write(row, col, Numeric_sheet[key])
            col += 1
        row += 1
print 'numeric done'


def write_Descriptor(df_all, wb, Links_list,Nodes_list):

    ws = wb.add_worksheet("Descriptor")

    DescriptorFields = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName',
                     'DescriptorValue']

    for i in range(len(DescriptorFields)):
        ws.write(0, i, DescriptorFields[i])

    row = 1

    # for df in df_all:

    Descriptor_list = []

    list1 = []

    for node in Nodes_list:
        list1.append({'InstanceName': node['InstanceName'], 'ObjectType': node['ObjectType']})
    for node in Links_list:
        list1.append({'InstanceName': node['InstanceName'], 'ObjectType': node['ObjectType']})

    for symbol_name, df in df_all.items():
        if symbol_name in ['y','wt','wsi_par_indx','wf_par_indx','v','t','sf_par_indx','s','run','rsi_indx','RA_par_indx','Qrun',
                       'NodeNotHeadwater','NodeNotDemandSite','n','MassBalanceNodes','j','fci_indx','dem'    ]:  #'QLoop' dReqBase,'evap'
            for i, itmes in df.iterrows():
                Instance_name = ''
                ObjectType = ''
                # append them together to be one new list

                Descriptor = OrderedDict()
                Descriptor['ObjectType'] = ObjectType
                Descriptor['InstanceName'] = Instance_name
                Descriptor['ScenarioName'] = ''
                Descriptor['AttributeName'] = symbol_name
                Descriptor['SourceName'] = ''
                Descriptor['MethodName'] = ''
                Descriptor['DescriptorValue'] = itmes[0]
                Descriptor_list.append(Descriptor)

    for Descriptor_sheet in Descriptor_list:
        col = 0
        for key in Descriptor_sheet.keys():
            ws.write(row, col, Descriptor_sheet[key])
            col += 1
        row += 1

print 'descriptor done'





def write_Seasonal(df_all, wb,Nodes_list,Links_list):



    ws = wb.add_worksheet("Seasonal")


    SeasonalFields = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName',
                      'SeasonName', 'SeasonNameCV', 'SeasonValue']

    for i in range(len(SeasonalFields)):
        ws.write(0, i, SeasonalFields[i])

    row = 1
    Seasonal_list=[]

    list1 = []

    for node in Nodes_list:
        list1.append({'InstanceName': node['InstanceName'], 'ObjectType': node['ObjectType']})
    for node in Links_list:
        list1.append({'InstanceName': node['InstanceName'], 'ObjectType': node['ObjectType']})

    for symbol_name, df in df_all.items():
        if symbol_name in ['Qmax','Qmin','aw','instreamReq','lss','Qsim','dReqBase','evap','reachGain']:
            for i, itmes in df.iterrows():
                # # add controlled vocabulary to each season shortcut name used in WEAP
                # if month_name == 'Oct':
                #     SeasonNameCV='October'
                # elif month_name == 'Nov':
                #     SeasonNameCV = 'November'
                # elif month_name == 'Dec':
                #     SeasonNameCV = 'December'
                # elif month_name == 'Jan':
                #     SeasonNameCV = 'January'
                # elif month_name == 'Feb':
                #     SeasonNameCV = 'February'
                # elif month_name == 'Mar':
                #     SeasonNameCV = 'March'
                # elif month_name == 'Apr':
                #     SeasonNameCV = 'April'
                # elif month_name == 'May':
                #     SeasonNameCV = 'May'
                # elif month_name == 'Jun':
                #     SeasonNameCV = 'June'
                # elif month_name == 'Jul':
                #     SeasonNameCV = 'July'
                # elif month_name == 'Aug':
                #     SeasonNameCV = 'August'
                # elif month_name == 'Sep':
                #     SeasonNameCV = 'September'

                if len(itmes)== 3: # for nodes
                    Instance_name=itmes[0]
                    ObjectType = ''
                else: # links
                    Instance_name=itmes[0]+itmes[1]
                    ObjectType = ''


                for instance_name_item in list1:
                    # look up the Object Type based on the given Instance name
                    if Instance_name == instance_name_item['InstanceName']:
                        ObjectType=instance_name_item['ObjectType']
                        break


                Seasonal = OrderedDict()
                Seasonal['ObjectType'] = ObjectType
                Seasonal['InstanceName'] = Instance_name
                Seasonal['ScenarioName'] = ''
                Seasonal['AttributeName'] = symbol_name
                Seasonal['SourceName'] = ''
                Seasonal['MethodName'] = ''
                if len(itmes) == 3:
                    Seasonal['SeasonName'] = itmes[1]#t1,t2 etc
                    Seasonal['SeasonValue'] = itmes[2]  # SeasonValue

                else:
                    Seasonal['SeasonName'] = itmes[2]#t1,t2 etc
                    Seasonal['SeasonValue'] = itmes[3]  # SeasonValue
                Seasonal['SeasonNameCV'] =''
                Seasonal_list.append(Seasonal)


    for SeasoanlSheet in Seasonal_list:
        col = 0
        for key in SeasoanlSheet.keys():
            ws.write(row, col, SeasoanlSheet[key])
            col += 1
        row += 1

    print 'seasonal done'


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
        if re['ExpresValueType'] == 'TimeSeries_ExpressValue':
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
                Resultx['DateTimeStamp'] = '{}-{}-1'.format(csv_data[0], csv_data[1])
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



def write_MultiAttributeSeries(df_all, wb,Nodes_list,Links_list):

    Upperfield_names = ['MultiAttributeSeriesName', 'AttributeName1', 'AttributeName2'
        , 'AttributeName3', 'AttributeName4', 'AttributeName5']

    ws = wb.add_worksheet("MultiAttributeSeries")

    for i, column_val in enumerate(Upperfield_names):
        # if i <4: continue
        ws.write(0, i+5, column_val)

    list1 = []
    for node in Nodes_list:
        list1.append({'InstanceName': node['InstanceName'], 'ObjectType': node['ObjectType']})
    for node in Links_list:
        list1.append({'InstanceName': node['InstanceName'], 'ObjectType': node['ObjectType']})

    Lowerfield_names = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName',
                        'MethodName', 'AttributeName1_Values', 'AttributeName2_Values'
        , 'AttributeName3_Values', 'AttributeName4_Values', 'AttributeName5_Values']
    LowerTable_list = []

    UpperTable_list = {}
    for symbol_name, df in df_all.items():

        # the problem of having this for-loop here is that the number of items can be 0,1,2 (so it depends on which symbol_name is used)

        UpperTable = OrderedDict()
        UpperTable['MultiAttributeSeriesName'] = symbol_name
        # if the paramter is for links and has t
        if symbol_name in ['fci_par','rsi_par','wsi_par','rv']:#'wf_par'  'RA_par','wght','wght'
            attr_list = []
            for i, items in df.iterrows():
                if len(items) > 3  and not items[3] in attr_list:
                    attr_list.append(items[3])

            UpperTable['AttributeName1'] = 't'  # t
            UpperTable['AttributeName2'] = attr_list[0]  # fci_par1
            if len(attr_list) > 1:
                UpperTable['AttributeName3'] = attr_list[1]  # fci_par2   # how to make it read the second key?
            if len(attr_list) > 2:
                UpperTable['AttributeName4'] = attr_list[2]  # fci_par3
            if len(attr_list) > 3:
                UpperTable['AttributeName5'] = attr_list[3]  # fci_par4
            UpperTable_list[symbol_name] = UpperTable

            series_name = ''
            LowerTable = None

            for i, items in df.iterrows():
                if series_name != items[2]:
                    if LowerTable != None:
                        LowerTable_list.append(LowerTable)
                        LowerTable = None

                    Instance_name = items[0] + items[1]
                    ObjectType = ''
                    # append them together to be one new list

                    for instance_name_item in list1:
                        # look up the Object Type based on the given Instance name
                        if Instance_name == instance_name_item['InstanceName']:
                            ObjectType = instance_name_item['ObjectType']
                            break
                    LowerTable = OrderedDict()
                    LowerTable['ObjectType'] = ObjectType
                    LowerTable['InstanceName'] = Instance_name
                    LowerTable['ScenarioName'] = ''
                    LowerTable['AttributeName'] = symbol_name
                    LowerTable['SourceName'] = ''
                    LowerTable['MethodName'] = ''
                    LowerTable['AttributeName1_Values'] = items[2]
                    for key in UpperTable.keys():
                        if key != 'MultiAttributeSeriesName' and key != 'AttributeName1':
                            LowerTable[UpperTable[key]] = ''
                    LowerTable[items[3]] = items[4]

                    series_name = items[2]
                else:
                    LowerTable[items[3]] = items[4]

            if LowerTable != None:
                LowerTable_list.append(LowerTable)

        ######################################################################
        # if no t  (in this case # of itemes is 0,1,2,3 (no t column)
        if symbol_name in ['wf_par']:  # 'wf_par'  'RA_par',
        # adapt exisitng code to habdle this case (no t)
            attr_list = []
            for i, items in df.iterrows():
                if len(items) > 2 and not items[2] in attr_list:
                    attr_list.append(items[2])

            UpperTable['AttributeName1'] = attr_list[0]  # fci_par1
            UpperTable['AttributeName2'] = attr_list[1]  # fci_par2
            if len(attr_list) > 2:
                UpperTable['AttributeName3'] = attr_list[2]  # fci_par3
            if len(attr_list) > 3:
                UpperTable['AttributeName4'] = attr_list[3]  # fci_par4
            UpperTable_list[symbol_name] = UpperTable

            Instance_name = ''
            LowerTable = None

            for i, items in df.iterrows():
                if (items[0] + items[1]) != Instance_name: # this one was working for the 't', I think (it
                    if LowerTable != None:
                        LowerTable_list.append(LowerTable)
                        LowerTable = None

                    Instance_name = items[0] + items[1]
                    ObjectType = ''
                    # append them together to be one new list

                    for instance_name_item in list1:
                        # look up the Object Type based on the given Instance name
                        if Instance_name == instance_name_item['InstanceName']:
                            ObjectType = instance_name_item['ObjectType']
                            break
                    LowerTable = OrderedDict()
                    LowerTable['ObjectType'] = ObjectType
                    LowerTable['InstanceName'] = Instance_name
                    LowerTable['ScenarioName'] = ''
                    LowerTable['AttributeName'] = symbol_name
                    LowerTable['SourceName'] = ''
                    LowerTable['MethodName'] = ''
                    for key in UpperTable.keys():
                        if key != 'MultiAttributeSeriesName':
                            LowerTable[UpperTable[key]] = ''
                    LowerTable[items[2]] = items[3]

                    # series_name = items[2]
                else:
                    LowerTable[items[2]] = items[3]

            if LowerTable != None:
                LowerTable_list.append(LowerTable)



        # # if the parameter is for nodes and no t (third conditon)
        if symbol_name in ['RA_par']:  # 'wf_par'  'RA_par',
        # # adapt exisiting code to handle this (no t) AND Instance_name = items[0] (Nodes only have one item)

            attr_list = []
            for i, items in df.iterrows():
                if len(items) > 2 and not items[1] in attr_list:
                    attr_list.append(items[1])

            UpperTable['AttributeName1'] = attr_list[0]  # fci_par1
            UpperTable['AttributeName2'] = attr_list[1]  # fci_par2
            if len(attr_list) > 2:
                UpperTable['AttributeName3'] = attr_list[2]  # fci_par3
            if len(attr_list) > 3:
                UpperTable['AttributeName4'] = attr_list[3]  # fci_par4
            UpperTable_list[symbol_name] = UpperTable

            Instance_name = ''
            LowerTable = None

            for i, items in df.iterrows():
                if (items[0] ) != Instance_name:
                    if LowerTable != None:
                        LowerTable_list.append(LowerTable)
                        LowerTable = None

                    Instance_name = items[0]
                    ObjectType = ''
                    # append them together to be one new list

                    for instance_name_item in list1:
                        # look up the Object Type based on the given Instance name
                        if Instance_name == instance_name_item['InstanceName']:
                            ObjectType = instance_name_item['ObjectType']
                            break
                    LowerTable = OrderedDict()
                    LowerTable['ObjectType'] = ObjectType
                    LowerTable['InstanceName'] = Instance_name
                    LowerTable['ScenarioName'] = ''
                    LowerTable['AttributeName'] = symbol_name
                    LowerTable['SourceName'] = ''
                    LowerTable['MethodName'] = ''
                    for key in UpperTable.keys():
                        if key != 'MultiAttributeSeriesName':
                            LowerTable[UpperTable[key]] = ''
                    LowerTable[items[1]] = items[2]

                    # series_name = items[2]
                else:
                    LowerTable[items[1]] = items[2]

            if LowerTable != None:
                LowerTable_list.append(LowerTable)




    row_upper = 1
    col = 5

    for symbol_name in UpperTable_list.keys():
        UpperTable = UpperTable_list[symbol_name]
        col=5
        for key in UpperTable.keys():
            ws.write(row_upper, col, UpperTable[key])
            col += 1
        row_upper += 1





    for i in range(len(Lowerfield_names)):
        ws.write(9, i, Lowerfield_names[i])



    row=10

    for LowerTable in LowerTable_list:
        col = 0
        for key in LowerTable.keys():
            ws.write(row, col, LowerTable[key])
            col += 1
        row += 1

    print 'done matrix'

        # n += 1

