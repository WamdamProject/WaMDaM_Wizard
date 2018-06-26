
# here we need to call the output from the Qurery functions

# df_TimeSeries
# df_MultiColumns
# df_Seasonal
# df_Numeric
# df_Descriptor
from collections import OrderedDict
import xlsxwriter
import datetime

################################### TimeSeries
def WriteMetadataFile(total_df_TimeSeries, total_df_Seasonal,total_df_MultiColumns,total_df_Numeric,total_df_Descriptor,
                      Metadata_TimeSeries , Metadata_seasonal,Metadata_multi_att,Metadata_multi_numeric,Metadata_multi_descriptor):

    # def WriteMetadataFile(multi_timeseries, multi_AttributeSeries, multi_Seasonal,
# def WriteMetadataFile(multi_timeseries, multi_AttributeSeries, multi_Seasonal,
#                       csv_file_name_timeseries, csv_file_path_or_value_seasonal,
#                       csv_file_path_or_value_multi):
#

    wb = xlsxwriter.Workbook('./WASH_InputFile_metadata.xlsx')
    ws = wb.add_worksheet()

    row = 0 # headers
    col = 0

    InputFile_list = []
    field_names = ['FullBranch', 'BranchType', 'BranchName', 'WaMDaM_VariableName','VariableName', 'Value', 'UnitName',
                   'MethodName', 'SourceName', 'SourcePerson', 'SoureOrganization', 'csv_file_Name',
                   'Date_exported']
    for i in range(len(field_names)):
        ws.write(0, i, field_names[i])

    Date_exported = datetime.datetime.now()

    for i, df_TimeSeries in enumerate(total_df_TimeSeries):
        # for csv_file_name in total_csv_file_name

        Result = OrderedDict()

        Result['FullBranch'] = Metadata_TimeSeries[i]['FullBranch']

        Result['BranchType'] = df_TimeSeries['ObjectType'][1]
        Result['BranchName'] = df_TimeSeries['NodeORLinkInstanceName'][1]
        Result['WaMDaM_VariableName'] = df_TimeSeries['AttributeName'][1]
        Result['VariableName'] = df_TimeSeries['AttributeName'][1].split('_')[0]

        Result['Value'] = Metadata_TimeSeries[i]['Value']

        Result['UnitName'] = df_TimeSeries['UnitName'][1]
        Result['MethodName'] = df_TimeSeries['MethodName'][1]
        Result['SourceName'] = df_TimeSeries['SourceName'][1]
        Result['SourcePerson'] = df_TimeSeries['SourcePerson'][1]
        Result['SoureOrganization'] = df_TimeSeries['SoureOrganization'][1]

        Result['csv_fileName'] = Metadata_TimeSeries[i]['csv_fileName']

        Result['Date_exported'] = Date_exported.strftime('%m/%d/%Y')

        InputFile_list.append(Result)
    #
    for i, df_Seasonal in enumerate(total_df_Seasonal):
        # for j in Metadata_seasonal:

        Result = OrderedDict()
        Result['FullBranch'] = Metadata_seasonal[i]['FullBranch']
        Result['BranchType'] = df_Seasonal['ObjectType'][1]
        Result['BranchName'] = df_Seasonal['NodeORLinkInstanceName'][1]
        Result['WaMDaM_VariableName']=df_Seasonal['AttributeName'][1]
        Result['VariableName'] = df_Seasonal['AttributeName'][1].split('_')[0]

        Result['Value'] = Metadata_seasonal[i]['Value']

        Result['UnitName'] = df_Seasonal['UnitName'][1]
        Result['MethodName'] = df_Seasonal['MethodName'][1]
        Result['SourceName'] = df_Seasonal['SourceName'][1]
        Result['SourcePerson'] = ''#df_Seasonal['SourcePerson'][1]
        Result['SoureOrganization'] =''# df_Seasonal['SoureOrganization'][1]
        Result['csv_fileName'] = Metadata_seasonal[i]['csv_fileName']
        Result['Date_exported'] = Date_exported.strftime('%m/%d/%Y')

        InputFile_list.append(Result)
    # #
    #
    for i, df_MultiColumns in enumerate(total_df_MultiColumns):
        Result = OrderedDict()

        Result['FullBranch'] =Metadata_multi_att[i]['FullBranch']

        Result['BranchType'] = df_MultiColumns['ObjectType'][1]
        Result['BranchName'] = df_MultiColumns['NodeORLinkInstanceName'][1]

        Result['WaMDaM_VariableName']=df_MultiColumns['MultiAttributeName'][1]
        Result['VariableName'] =df_MultiColumns['MultiAttributeName'][1].split('_')[0]

        Result['Value'] = Metadata_multi_att[i]['Value']

        Result['UnitName'] = df_MultiColumns['UnitName'][1]
        Result['MethodName'] = df_MultiColumns['MethodName'][1]
        Result['SourceName'] = df_MultiColumns['SourceName'][1]
        Result['SourcePerson'] = ''#df_MultiColumns['SourcePerson'][1]
        Result['SoureOrganization'] =''# df_MultiColumns['SoureOrganization'][1]

        Result['csv_fileName'] = Metadata_multi_att[i]['csv_fileName']

        Result['Date_exported'] = Date_exported.strftime('%m/%d/%Y')

        InputFile_list.append(Result)



    for i, df_Numeric in enumerate(total_df_Numeric):
        Result = OrderedDict()

        Result['FullBranch'] =Metadata_multi_numeric[i]['FullBranch']

        Result['BranchType'] = df_Numeric['ObjectType'][0]
        Result['BranchName'] = df_Numeric['NodeORLinkInstanceName'][0]

        Result['WaMDaM_VariableName']=df_Numeric['AttributeName'][0]
        Result['VariableName'] =df_Numeric['AttributeName'][0].split('_')[0]

        Result['Value'] = df_Numeric['Value'][0]

        Result['UnitName'] = df_Numeric['UnitName'][0]
        Result['MethodName'] = df_Numeric['MethodName'][0]
        Result['SourceName'] = df_Numeric['SourceName'][0]
        Result['SourcePerson'] = ''#df_MultiColumns['SourcePerson'][0]
        Result['SoureOrganization'] =''# df_MultiColumns['SoureOrganization'][0]

        Result['csv_fileName'] = Metadata_multi_numeric[i]['csv_fileName']

        Result['Date_exported'] = Date_exported.strftime('%m/%d/%Y')

        InputFile_list.append(Result)



    for i, df_Descriptor in enumerate(total_df_Descriptor):
        Result = OrderedDict()

        Result['FullBranch'] =Metadata_multi_descriptor[i]['FullBranch']

        Result['BranchType'] = df_Descriptor['ObjectType'][0]
        Result['BranchName'] = df_Descriptor['NodeORLinkInstanceName'][0]

        Result['WaMDaM_VariableName']=df_Descriptor['AttributeName'][0]
        Result['VariableName'] =df_Descriptor['AttributeName'][0].split('_')[0]

        Result['Value'] = df_Descriptor['Value'][0]

        Result['UnitName'] = df_Descriptor['UnitName'][0]
        Result['MethodName'] = df_Descriptor['MethodName'][0]
        Result['SourceName'] = df_Descriptor['SourceName'][0]
        Result['SourcePerson'] = ''#df_MultiColumns['SourcePerson'][0]
        Result['SoureOrganization'] =''# df_MultiColumns['SoureOrganization'][0]

        Result['csv_fileName'] = Metadata_multi_descriptor[i]['csv_fileName']

        Result['Date_exported'] = Date_exported.strftime('%m/%d/%Y')

        InputFile_list.append(Result)


    for row, Result in enumerate(InputFile_list):
        col = 0
        for key in Result.keys():
            ws.write(row+1, col, Result[key])
            col += 1

    wb.close()

    return InputFile_list


