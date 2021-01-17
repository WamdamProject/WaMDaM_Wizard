
# here we need to call the output from the Qurery functions

# df_TimeSeries
# df_MultiColumns
# df_Seasonal
# df_Numeric
# df_Descriptor
from collections import OrderedDict
import xlsxwriter
import datetime
import pandas as pd
################################### TimeSeries
def WriteMetadataFile(WEAPAreasDirectory,total_df_TimeSeries, total_df_Seasonal,total_df_MultiColumns,total_df_Numeric,total_df_Descriptor,
                      Metadata_TimeSeries , Metadata_seasonal,Metadata_multi_att,Metadata_multi_numeric,Metadata_multi_descriptor):

    # def WriteMetadataFile(multi_timeseries, multi_AttributeSeries, multi_Seasonal,
# def WriteMetadataFile(multi_timeseries, multi_AttributeSeries, multi_Seasonal,
#                       csv_file_name_timeseries, csv_file_path_or_value_seasonal,
#                       csv_file_path_or_value_multi):
#
    #
    # wb = xlsxwriter.Workbook(WEAPAreasDirectory+'\WEAP_InputFile_metadata.xlsx')
    # ws = wb.add_worksheet()
    #
    # row = 0 # headers
    # col = 0
    # field_names = ['BranchType', 'BranchName', 'WaMDaM_VariableName','VariableName', 'Value', 'UnitName',

    InputFile_list = []
    field_names = ['BranchType', 'BranchName', 'VariableName', 'Value', 'UnitName',
                   'MethodName', 'SourceName', 'SourcePerson', 'SoureOrganization', 'csv_file_Name',
                   'Date_exported']
    # for i in range(len(field_names)):
    #     ws.write(0, i, field_names[i])

    Date_exported = datetime.datetime.now()

    for metadata,df_TimeSeries in zip(Metadata_TimeSeries,total_df_TimeSeries):
        # for csv_file_name in total_csv_file_name

        Result = OrderedDict()


        Result['BranchType'] = df_TimeSeries['ObjectType'][1]
        Result['BranchName'] = df_TimeSeries['InstanceName'][1]
        # Result['WaMDaM_VariableName'] = df_TimeSeries['AttributeName_Abstract'][1]
        # Result['VariableName'] = df_TimeSeries['AttributeName'][1].split('_')[0]
        Result['VariableName'] = df_TimeSeries['AttributeName_Abstract'][1]

        Result['Value'] = metadata['Value']

        Result['UnitName'] = df_TimeSeries['UnitName'][1]
        Result['MethodName'] = df_TimeSeries['MethodName'][1]
        Result['SourceName'] = df_TimeSeries['SourceName'][1]
        Result['SourcePerson'] = df_TimeSeries['SourcePerson'][1]
        Result['SoureOrganization'] = df_TimeSeries['SoureOrganization'][1]

        Result['csv_fileName'] =metadata['csv_fileName']

        Result['Date_exported'] = Date_exported.strftime('%m/%d/%Y')

        InputFile_list.append(Result)
    #
    for metadata_seasonal,df_Seasonal in zip(Metadata_seasonal,total_df_Seasonal):
        # for j in Metadata_seasonal:

        Result = OrderedDict()
        Result['BranchType'] = df_Seasonal['ObjectType'][1]
        Result['BranchName'] = df_Seasonal['InstanceName'][1]
        # Result['WaMDaM_VariableName']=df_Seasonal['AttributeName'][1]
        # Result['VariableName'] = df_Seasonal['AttributeName'][1].split('_')[0]
        Result['VariableName'] = df_Seasonal['AttributeName_Abstract'][1]

        Result['Value'] = metadata_seasonal['Value']

        Result['UnitName'] = df_Seasonal['UnitName'][1]
        Result['MethodName'] = df_Seasonal['MethodName'][1]
        Result['SourceName'] = df_Seasonal['SourceName'][1]
        Result['SourcePerson'] = ''#df_Seasonal['SourcePerson'][1]
        Result['SoureOrganization'] =''# df_Seasonal['SoureOrganization'][1]
        Result['csv_fileName'] = metadata_seasonal['csv_fileName']
        Result['Date_exported'] = Date_exported.strftime('%m/%d/%Y')

        InputFile_list.append(Result)
    # #
    #
    for metadata_multi,df_MultiColumns in zip(Metadata_multi_att,total_df_MultiColumns):
        Result = OrderedDict()


        Result['BranchType'] = df_MultiColumns['ObjectType'][1]
        Result['BranchName'] = df_MultiColumns['InstanceName'][1]

        # Result['WaMDaM_VariableName']=df_MultiColumns['MultiAttributeName'][1]
        # Result['VariableName'] =df_MultiColumns['MultiAttributeName'][1].split('_')[0]
        Result['VariableName'] = df_MultiColumns['AttributeName_Abstract'][1]

        Result['Value'] = metadata_multi['Value']

        Result['UnitName'] = df_MultiColumns['UnitName'][1]
        Result['MethodName'] = df_MultiColumns['MethodName'][1]
        Result['SourceName'] = df_MultiColumns['SourceName'][1]
        Result['SourcePerson'] = ''#df_MultiColumns['SourcePerson'][1]
        Result['SoureOrganization'] =''# df_MultiColumns['SoureOrganization'][1]

        Result['csv_fileName'] = metadata_multi['csv_fileName']

        Result['Date_exported'] = Date_exported.strftime('%m/%d/%Y')

        InputFile_list.append(Result)



    for df_Numeric in total_df_Numeric:
        Result = OrderedDict()


        Result['BranchType'] = df_Numeric['ObjectType'][0]
        Result['BranchName'] = df_Numeric['InstanceName'][0]

        # Result['WaMDaM_VariableName']=df_Numeric['AttributeName'][0]
        # Result['VariableName'] =df_Numeric['AttributeName'][0].split('_')[0]
        Result['VariableName'] = df_Numeric['AttributeName_Abstract'][0]

        Result['Value'] = df_Numeric['Value'][0]

        Result['UnitName'] = df_Numeric['UnitName'][0]
        Result['MethodName'] = df_Numeric['MethodName'][0]
        Result['SourceName'] = df_Numeric['SourceName'][0]
        Result['SourcePerson'] = ''#df_MultiColumns['SourcePerson'][0]
        Result['SoureOrganization'] =''# df_MultiColumns['SoureOrganization'][0]

        Result['csv_fileName'] =''# Metadata_multi_numeric[i]['csv_fileName']

        Result['Date_exported'] = Date_exported.strftime('%m/%d/%Y')

        InputFile_list.append(Result)



    for df_Descriptor in total_df_Descriptor:
        Result = OrderedDict()


        Result['BranchType'] = df_Descriptor['ObjectType'][0]
        Result['BranchName'] = df_Descriptor['InstanceName'][0]

        # Result['WaMDaM_VariableName']=df_Descriptor['AttributeName'][0]
        # Result['VariableName'] =df_Descriptor['AttributeName'][0].split('_')[0]
        Result['VariableName'] = df_Descriptor['AttributeName_Abstract'][0]

        Result['Value'] = df_Descriptor['Value'][0]

        Result['UnitName'] = df_Descriptor['UnitName'][0]
        Result['MethodName'] = df_Descriptor['MethodName'][0]
        Result['SourceName'] = df_Descriptor['SourceName'][0]
        Result['SourcePerson'] = ''#df_MultiColumns['SourcePerson'][0]
        Result['SoureOrganization'] =''# df_MultiColumns['SoureOrganization'][0]

        Result['csv_fileName'] = ''#Metadata_multi_descriptor[i]['csv_fileName']

        Result['Date_exported'] = Date_exported.strftime('%m/%d/%Y')

        InputFile_list.append(Result)

    InputFile_df = pd.DataFrame(data=InputFile_list)
    InputFile_df.to_excel(WEAPAreasDirectory+'\WEAP_InputFile_metadata.xlsx',sheet_name = 'Metadata',index=False)

    print 'Saved the input data metadata file'
    return InputFile_list


