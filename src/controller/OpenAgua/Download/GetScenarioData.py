 #########################################################################################################################################3

    # loop through the scenarios (if more than one is available)
    # first get the Parent Scenario and get its data and process it below
    # second, loop though the child scenarios and if they have data, overwrite the parent data
    # append the data for all the scenarios together and print them one time to the sheets

    ##################################################################################################################
    # Get and process scenario data
    ##################################################################################################################
    # reset the scenario ID to pass it with its children as well

from pandas.io.json import json_normalize
import pandas as pd
from datetime import datetime
import json

def GetScenarioData(Selected_scenario_ids,conn,Selected_network_id,Attribute_Frame_df,ObjectType_lst):

    FreeText_data_header = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName']

    FreeText_data_result = []
    NumericValue_data_result = []
    TimeSeriesValues_data_result = []
    TimeSeries_data_result = []
    array_data_result = []
    SeasonalValues = []
    FreeText_data_result_all = []
    NumericValue_data_result_all = []
    TimeSeries_data_result_all = []
    TimeSeriesValues_data_result_all = []
    array_data_result_all = []

    FreeText_data_header = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName']

    TimeSeriesValues_header = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName']

    Timseries_header = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName',
                        'YearType',
                        'AggregationStatisticCV', 'AggregationInterval', 'IntervalTimeUnit', 'IsRegular', 'NoDataValue',
                        'Description']

    Seasonal_header = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName']


    YearType='CalenderYear'
    AggregationStatisticCV='Average'
    AggregationInterval=1
    IntervalTimeUnit='month'
    IsRegular=''
    NoDataValue='-9999'
    Description=''
    ScenarioStartMonth=''
    ParentScenario=Selected_scenario_ids[0]

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    ParentResource_data_result = conn.call('get_all_resource_data',
                                           {'network_id': Selected_network_id, 'scenario_id': ParentScenario,
                                            'include_values': 'Y', 'include_metadata': 'Y'})

    ParentResource_data_result_df = json_normalize(ParentResource_data_result)
    Scenario = conn.call('get_scenario', {'scenario_id': ParentScenario})

    ScenarioStartDate = Scenario['start_time']
    ScenarioStartMonth = datetime.strptime(ScenarioStartDate, '%Y-%m-%d %H:%M:%S').month
    print ScenarioStartMonth
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    Selected_scenario_id=[]
    for Selected_scenario_id in Selected_scenario_ids:
        # print Selected_scenario_id
        # The first scenario is always the parent. It has the full data
        # use the same data for all the childs.
        # if a child has new different data, then we overwrite the parent data
#########################################################################################################################################3
        Scenario=conn.call('get_scenario',{'scenario_id': Selected_scenario_id})
        ScenarioName = Scenario['name']

        Child_Resource_data_result = conn.call('get_all_resource_data',
                                         {'network_id': Selected_network_id, 'scenario_id': Selected_scenario_id,
                                          'include_values': 'Y', 'include_metadata': 'Y'})
        Child_Resource_data_result_df = json_normalize(Child_Resource_data_result)
        # iterate over the parent

        for index, row in ParentResource_data_result_df.iterrows():
            # for each row in parent, compare it with all the child rows
            MethodName = 'AddMethodName'

            for index_child, row_child in Child_Resource_data_result_df.iterrows():
                # if child row exist and matches the row parent metadata, then overwrite the row and index values with the child's data
                if row['resource_attr_id'] == row_child['resource_attr_id']:
                    if row['dataset_id'] != row_child['dataset_id']:
                        print 'diff value'
                        index=index_child
                        row=row_child
                        # changing the method name from the other scenarios is needed
                        #  to compare differences
                        # MethodName='AddScenario_MethodName'

                    else:
                        pass

            ObjectTyplology=row['ref_key']
            InstanceName = row['ref_name']
            ObjectType = ''
            # if row['attr_name']=='Demand' and row['ref_name']=='DR Bajo Rio San Juan':

            if (InstanceName, ObjectTyplology) in ObjectType_lst.keys():  # here we need to also use "Node" or "Link" or "Network" in addition to Instance Name
                # Look up the ObjectType in the NodesData_df using the InstanceName
                ObjectType= ObjectType_lst[(InstanceName,ObjectTyplology)]

                # check if the attribute does not exist for this Object Type in the Attributes table.
                # if it does not exist then continue the for loop (to skip the rest of he code)
                AttributeName = row['attr_name']
                DatasetAttributeID= str(row['attr_id'])

                # exist_row = Attribute_Frame_df[(Attribute_Frame_df.ObjectType == ObjectType) &
                #                                (Attribute_Frame_df.AttributeName == AttributeName)
                #                                 & ([str(x) for x in Attribute_Frame_df.AttributeID.tolist()] == DatasetAttributeID)]
                for attr_row in Attribute_Frame_df.iterrows():
                #     if not (attr_row[1]['ObjectType']==ObjectType and \
                #         attr_row[1]['AttributeName'] == AttributeName and \
                    if not (DatasetAttributeID==str(attr_row[1]['AttributeID'])
                            and attr_row[1]['ObjectType']==ObjectType and
                            attr_row[1]['AttributeName'] == AttributeName):
                        continue

                    # get metadata
                    dataset_metadata = json.loads(row['dataset_metadata'])

                    if not 'source' in  dataset_metadata.keys():
                        SourceName='AddSourceName'
                    else:
                        SourceName=dataset_metadata['source']

                    if not 'method' in  dataset_metadata.keys():
                        MethodName=MethodName
                    else:
                        MethodName=dataset_metadata['method']

                    # ValuesSheets['ScenarioName']=row['ref_name']

                    # AttributeName = row['attr_name']
                    #######################################################
                    # Get the data values and prepare them for WaMDaM for each data type
                    #######################################################

                    if row['dataset_type']=='descriptor':
                        if row['dataset_value']:
                            FreeText_value = row['dataset_value']
                        else:
                            FreeText_value='Empty_in_OpenAgua'

                        output_row = []
                        for header in FreeText_data_header:
                            if header == "InstanceName":
                                output_row.append(InstanceName)
                            elif header == "ObjectType":
                                output_row.append(ObjectType)
                            elif header == "AttributeName":
                                output_row.append(AttributeName)
                            elif header == 'ScenarioName':
                                output_row.append(ScenarioName)
                            elif header == 'SourceName':
                                output_row.append(SourceName)
                            elif header == 'MethodName':
                                output_row.append(MethodName)
                            else:
                                output_row.append('')

                        output_row.append(FreeText_value)
                        FreeText_data_result.append(output_row)


                    if row['dataset_type']=='scalar':
                        NumericValue_value=str(row['dataset_value'])
                        output_row = []
                        for header in FreeText_data_header:
                            if header == "InstanceName":
                                output_row.append(InstanceName)

                            elif header == "ObjectType":
                                output_row.append(ObjectType)

                            elif header == "AttributeName":
                                output_row.append(AttributeName)

                            elif header == 'ScenarioName':
                                output_row.append(ScenarioName)

                            elif header == 'SourceName':
                                output_row.append(SourceName)

                            elif header == 'MethodName':
                                output_row.append(MethodName)
                            else:
                                output_row.append('')

                        output_row.append(NumericValue_value)
                        if output_row=='':
                            output_row='-9999'
                        NumericValue_data_result.append(output_row)


                    if row['dataset_type']=='timeseries':
                        json_times = json.loads(row['dataset_value'])
                        for key in json_times.keys():
                            if key == 'Header' :  continue
                            all_monthes = {}
                            for time in sorted(json_times[key].keys()):
                                value = json_times[key][time]

                                output_row = []
                                output_row_times = []
                                year = time.split('T')[0]
                                if not '9998' in year and not '9999' in year:  # these years indicate sesonal data
                                    for header in TimeSeriesValues_header:
                                        if header == "InstanceName":
                                            output_row.append(InstanceName)
                                        elif header == "ObjectType" :
                                            output_row.append(ObjectType)
                                        elif header == "AttributeName" :
                                            output_row.append(AttributeName)
                                        elif header == 'ScenarioName':
                                            output_row.append(ScenarioName)
                                        else:
                                            output_row.append('')
                                    output_row.append(datetime.strptime(time.split('T')[0], '%Y-%m-%d').strftime("%Y/%m/%d")) ### format MM/DD/YYYY  1975-12-01T00:00:00.000000000Z
                                    if value == '' or value==None:
                                        value = '-9999'
                                    value = str(value)
                                    output_row.append(value)
                                    TimeSeriesValues_data_result.append(output_row)

                                    # Add 4_TimeSeries sheet

                                    for header in Timseries_header:
                                        if header == "InstanceName":
                                            output_row_times.append(InstanceName)

                                        elif header == "ObjectType":
                                            output_row_times.append(ObjectType)

                                        elif header == 'SourceName':
                                            output_row_times.append(SourceName)
                                        elif header == 'MethodName':
                                            output_row_times.append(MethodName)

                                        elif header == "AttributeName":
                                            output_row_times.append(AttributeName)
                                        elif header == 'ScenarioName':
                                            output_row_times.append(ScenarioName)
                                        else:
                                            output_row_times.append('')



                                    # write the unqiue ObjectType, InstanceName,ScenarioName,AttributeName to this sheet
                                    # Use the values below that are provided above
                                    output_row_times[6] = YearType
                                    output_row_times[7] =AggregationStatisticCV
                                    output_row_times[8] =AggregationInterval
                                    output_row_times[9] =IntervalTimeUnit
                                    output_row_times[10] =IsRegular
                                    output_row_times[11] =NoDataValue
                                    output_row_times[12] =Description
                                    TimeSeries_data_result.append(output_row_times)

                                else:
                                    time = datetime.strptime(time.split('T')[0], '%Y-%m-%d').strftime("%Y/%m/%d")
                                    for header in Seasonal_header:
                                        if header == "InstanceName":
                                            output_row.append(InstanceName)

                                        elif header == "ObjectType":
                                            output_row.append(ObjectType)

                                        elif header == "AttributeName":
                                            output_row.append(AttributeName)
                                        elif header == 'ScenarioName':
                                            output_row.append(ScenarioName)
                                        elif header == 'SourceName':
                                            output_row.append(SourceName)
                                        elif header == 'MethodName':
                                            output_row.append(MethodName)
                                        else:
                                            output_row.append('')

                                    SeasonName = ''
                                    SeasonNameCV = ''
                                    Order = 1

                                    if ScenarioStartMonth==10:
                                        if time == '9998/10/01':
                                            SeasonName = 'Oct'
                                            SeasonNameCV = 'October'
                                            Order=1

                                        elif time == '9998/11/01':
                                            SeasonName = 'Nov'
                                            SeasonNameCV = 'November'
                                            Order=2


                                        elif time == '9998/12/01':
                                            SeasonName = 'Dec'
                                            SeasonNameCV = 'December'
                                            Order=3


                                        elif time == '9999/01/01':
                                            SeasonName = 'Jan'
                                            SeasonNameCV = 'January'
                                            Order=4


                                        elif time == '9999/02/01':
                                            SeasonName = 'Feb'
                                            SeasonNameCV = 'February'
                                            Order=5


                                        elif time == '9999/03/01':
                                            SeasonName = 'Mar'
                                            SeasonNameCV = 'March'
                                            Order=6


                                        elif time == '9999/04/01':
                                            SeasonName = 'Apr'
                                            SeasonNameCV = 'April'
                                            Order=7

                                        elif time == '9999/05/01':
                                            SeasonName = 'May'
                                            SeasonNameCV = 'May'
                                            Order=8


                                        elif time == '9999/06/01':
                                            SeasonName = 'Jun'
                                            SeasonNameCV = 'June'
                                            Order=9


                                        elif time == '9999/07/01':
                                            SeasonName = 'Jul'
                                            SeasonNameCV = 'July'
                                            Order=10

                                        elif time == '9999/08/01':
                                            SeasonName = 'Aug'
                                            SeasonNameCV = 'August'
                                            Order=11


                                        elif time == '9999/09/01':
                                            SeasonName = 'Sep'
                                            SeasonNameCV = 'September'
                                            Order=12

                                    elif ScenarioStartMonth==1:

                                        if time == '9999/01/01':
                                            SeasonName = 'Jan'
                                            SeasonNameCV = 'January'
                                            Order = 1


                                        elif time == '9999/02/01':
                                            SeasonName = 'Feb'
                                            SeasonNameCV = 'February'
                                            Order = 2


                                        elif time == '9999/03/01':
                                            SeasonName = 'Mar'
                                            SeasonNameCV = 'March'
                                            Order = 3


                                        elif time == '9999/04/01':
                                            SeasonName = 'Apr'
                                            SeasonNameCV = 'April'
                                            Order = 4

                                        elif time == '9999/05/01':
                                            SeasonName = 'May'
                                            SeasonNameCV = 'May'
                                            Order = 5


                                        elif time == '9999/06/01':
                                            SeasonName = 'Jun'
                                            SeasonNameCV = 'June'
                                            Order = 6


                                        elif time == '9999/07/01':
                                            SeasonName = 'Jul'
                                            SeasonNameCV = 'July'
                                            Order = 7

                                        elif time == '9999/08/01':
                                            SeasonName = 'Aug'
                                            SeasonNameCV = 'August'
                                            Order = 8


                                        elif time == '9999/09/01':
                                            SeasonName = 'Sep'
                                            SeasonNameCV = 'September'
                                            Order = 9

                                        elif time == '9999/10/01':
                                            SeasonName = 'Oct'
                                            SeasonNameCV = 'October'
                                            Order = 10

                                        elif time == '9999/11/01':
                                            SeasonName = 'Nov'
                                            SeasonNameCV = 'November'
                                            Order = 11


                                        elif time == '9999/12/01':
                                            SeasonName = 'Dec'
                                            SeasonNameCV = 'December'
                                            Order = 12

                                    output_row.append(SeasonName)
                                    output_row.append(SeasonNameCV)
                                    if value=='':
                                        value=0
                                    output_row.append(value)
                                    all_monthes[Order] = output_row

                            keylist = all_monthes.keys()
                            keylist.sort()
                            for key in keylist:
                                SeasonalValues.append(all_monthes[key])


                    if row['dataset_type']=='array':
                        json_array = json.loads(row['dataset_value'])
                        for index, item in enumerate(json_array[0]):
                            output_row = []
                            for header in FreeText_data_header:
                                if header == "InstanceName":
                                    output_row.append(InstanceName)

                                elif header == "ObjectType":
                                    output_row.append(ObjectType)

                                elif header == "AttributeName":
                                    output_row.append(AttributeName)

                                elif header == 'ScenarioName':
                                    output_row.append(ScenarioName)
                                elif header == 'SourceName':
                                    output_row.append(SourceName)
                                elif header == 'MethodName':
                                    output_row.append(MethodName)
                                else:
                                    output_row.append('')
                            for i in range(0, 6):
                                try:
                                    value = json_array[i][index]
                                    value = str(value)

                                except:
                                    value = ''
                                output_row.append(value)
                            array_data_result.append(output_row)




        # here append all the results for all the scenarios


        FreeText_data_result_all.extend(FreeText_data_result)
        NumericValue_data_result_all.extend(NumericValue_data_result)
        TimeSeries_data_result_all.extend(TimeSeries_data_result)
        TimeSeriesValues_data_result_all.extend(TimeSeriesValues_data_result)
        array_data_result_all.extend(array_data_result)


    # save the result to data frames

    FreeText_data_header.append('FreeText')  # it shows "numeric" in the last column but should be FreeText

    FreeText_frame_result = pd.DataFrame(FreeText_data_result, columns=FreeText_data_header)


    FreeText_data_header.pop(-1)

    FreeText_data_header.append('NumericValue')  # this one should be for Numric not

    NumericValue_frame_result = pd.DataFrame(NumericValue_data_result, columns=FreeText_data_header)

    TimeSeriesValues_header.append('DateTimeStamp')
    TimeSeriesValues_header.append('Value')
    TimeSeriesValues_frame_result = pd.DataFrame(TimeSeriesValues_data_result, columns=TimeSeriesValues_header)

    TimeSeriesValues_frame_result = TimeSeriesValues_frame_result.sort_values(
        ['ScenarioName','ObjectType', 'InstanceName',
         'AttributeName', 'DateTimeStamp'], ascending =True)

    TimeSeriesValues_frame_result['DateTimeStamp'] = pd.to_datetime(TimeSeriesValues_frame_result.DateTimeStamp).apply(
        lambda x: x.strftime('%m/%d/%Y'))



    # Here, lets get the unique rows based on the ObjectType', 'InstanceName', 'ScenarioName',  AttributeName
    Times_frame_result = pd.DataFrame(TimeSeries_data_result, columns=Timseries_header)
    Times_frame_result = Times_frame_result.drop_duplicates()


    Seasonal_header.append('SeasonName')
    Seasonal_header.append('SeasonNameCV')
    Seasonal_header.append('SeasonValue')
    SeasonalValues_df = pd.DataFrame(SeasonalValues, columns=Seasonal_header)

    FreeText_data_header.pop(-1)
    for i in range(1, 7):
        header_name = 'AttributeName{}_Values'.format(i)
        FreeText_data_header.append(header_name)
    array_frame_result = pd.DataFrame(array_data_result, columns=FreeText_data_header)

    muti_header = ['MultiAttributeSeriesName', 'AttributeName1', 'AttributeName2', 'AttributeName3', 'AttributeName4',
                   'AttributeName_Column5', 'AttributeName_Column6']
    up_frame_data = pd.DataFrame([], columns=muti_header)



    return FreeText_frame_result,NumericValue_frame_result,SeasonalValues_df, \
           Times_frame_result,TimeSeriesValues_frame_result,up_frame_data,array_frame_result