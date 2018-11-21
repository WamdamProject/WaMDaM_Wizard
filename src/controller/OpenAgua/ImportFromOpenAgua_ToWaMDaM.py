from controller.OpenAgua.HydraLib.PluginLib import JsonConnection, \
    create_xml_response, \
    write_progress, \
    write_output
from collections import OrderedDict

# General library for working with JSON objects
import json
# Used for working with files.
import os, sys
from datetime import datetime
import logging

from controller.WriteWaMDaMToExcel.ExportTemplate import ExportTemplate

from pandas.io.json import json_normalize
import pandas as pd



def ImportData(conn,Selected_template_id, Selected_network_id, Selected_scenario_id, ExportFilePath,GlobalAttributesID):

    # hard coded metadata can be upated here. Right now, they dont exist in Hydra/OpenAgua.
    # future work will allow a systematic way to define these metadata items in Hydra which then allows us to import them back to WaMDaM

    MethodName='AddMethodName'
    SourceName='AddSourceName'

    exportTemplate = ExportTemplate(ExportFilePath)


    Template=conn.call('get_template',{'template_id':Selected_template_id})

    Scenario=conn.call('get_scenario',{'scenario_id': Selected_scenario_id})
    ScenarioName=Scenario['name']
    EndTime=''
    # -----------------------------------------
    columns_ResourceType=['ResourceType',	'ResourceTypeAcronym','MethodName','Description']

    columns_ObjecTypes = ['ObjectType','ObjectTypology','DatasetAcronym','ObjectTypeCV','Layout','ObjectCategory','Description']


    columns_Attributes = ['ObjectType','AttributeName','AttributeName_Abstract','AttributeNameCV','AttributeUnit','AttributeUnitCV',
                          'AttributeDataTypeCV','AttributeCategory','ModelInputOrOutput','AttributeDescription','AttributeScale']
    ResourceType_top_data = []
    ResourceType_bottom_data = []
    Attributes_data_result = []

    ResourceType = Template['name']
    DatasetAcronym = Template['name']
    Description = []
    top_row = []


    for header in columns_ResourceType:
        if 'ResourceType' == header:
            top_row.append(ResourceType)
        elif header == 'ResourceTypeAcronym':
            top_row.append(DatasetAcronym)
        else:
            top_row.append('')
    ResourceType_top_data.append(top_row)

    for key in Template.keys():
        if key=='types':
            Types = Template[key]
            for type in Types:
                if ((type['id']==GlobalAttributesID and type['resource_type']=='NETWORK') or \
                        (type['resource_type']=='NODE') or (type['resource_type'] == 'LINK')):

                    ObjectType = type['name']
                    if type['resource_type']=='NODE':
                        ObjectTypology ='Node'
                    elif  type['resource_type']=='LINK':
                        ObjectTypology = 'Link'
                    elif type['resource_type']=='NETWORK':
                        ObjectTypology = 'Network'
                    else:
                        ObjectTypology=''

                    ObjectTypology=ObjectTypology
                    ObjectTypeID=type['id']
                    DatasetAcronym=DatasetAcronym
                    ObjectTypeCV=[]
                    Layout=json.dumps(type['layout'])[1:-1]
                    ObjectCategory=[]
                    Description=[]

                    bottom_row = []
                    for header in columns_ObjecTypes:
                        if 'ObjectType' ==  header:
                            bottom_row.append(ObjectType)
                        elif 'ObjectTypology' == header:
                            bottom_row.append(ObjectTypology)
                        elif 'DatasetAcronym' == header:
                            bottom_row.append(DatasetAcronym)
                        elif 'Layout' == header:
                            bottom_row.append(Layout)
                        else:
                            bottom_row.append('')
                    ResourceType_bottom_data.append(bottom_row)


                    Types = Template[key]
                    if 'typeattrs' in type.keys() :
                        Types = Template[key]
                        TypeAttr=''
                        for attr in type['typeattrs']:
                            attribute_row = []
                            ObjectType=ObjectType
                            AttributeName=attr['attr_name']
                            AttributeName_Abstract=attr['attr_name']
                            AttributeNameCV=[]


                            AttributeUnit=attr['unit']  # [unit]default_dataset

                            AttributeUnitCV='' # """ GET the UNIT """

                            if not 'category' in attr['properties'].keys():
                                AttributeCategory=''
                            else:
                                AttributeCategory = attr['properties']['category']

                            if not 'scale' in attr['properties'].keys():
                                AttributeScale = ''
                            else:
                                AttributeScale=attr['properties']['scale']

                            Dimension = attr['dimension']

                            if attr['data_type']=='array':
                                AttributeDataTypeCV = 'MultiAttributeSeries'

                            elif attr['data_type']=='periodic timeseries':
                                AttributeDataTypeCV = 'SeasonalNumericValues'

                            elif attr['data_type']=='scalar':
                                AttributeDataTypeCV = 'NumericValues'

                            elif attr['data_type']== 'timeseries':
                                AttributeDataTypeCV = 'TimeSeries'

                            elif attr['data_type']== 'descriptor':
                                AttributeDataTypeCV = 'FreeText'


                            ModelInputOrOutput=[]
                            AttributeDescription=[]


                            for header in columns_Attributes:
                                if 'ObjectType' == header:
                                    attribute_row.append(ObjectType)
                                elif 'AttributeName' == header:
                                    attribute_row.append(AttributeName)
                                elif 'AttributeName_Abstract' == header:
                                    attribute_row.append(AttributeName_Abstract)
                                elif 'AttributeDataTypeCV' == header:
                                    attribute_row.append(AttributeDataTypeCV)
                                elif 'AttributeUnitCV' == header:
                                    attribute_row.append(AttributeUnitCV)
                                elif 'AttributeUnit' == header:
                                    attribute_row.append(AttributeUnit)
                                elif 'AttributeCategory' == header:
                                    attribute_row.append(AttributeCategory)
                                elif 'AttributeScale' == header:
                                    attribute_row.append(AttributeScale)
                                else:
                                    attribute_row.append('')

                            Attributes_data_result.append(attribute_row)


    ResourceType_Top_df=pd.DataFrame(ResourceType_top_data, columns=columns_ResourceType)

   # sort the Object types
    custom_dict = ['Network', 'Node', 'Link']

    sort_list = {}
    for row in ResourceType_bottom_data:
        if not row[1] in sort_list.keys():
            sort_list[row[1]] = [row]
        else:
            sort_list[row[1]].append(row)

    total_list = []
    for key in custom_dict:
        if len(total_list) < 1 and key in sort_list.keys():
            total_list = sort_list[key]
        elif key in sort_list.keys():
            total_list.extend(sort_list[key])

    # total_list
    #
    # if ObjectType=='Network':
    #
    #
    # ResourceTypeAcronym + ' Global Attributes'

    ResourceType_Bottom_df = pd.DataFrame(total_list, columns=columns_ObjecTypes)



    People_headers = ["PersonName", "Address", "Email", "Phone", "PersonWebpage", "Position", "OrganizationName"]
    Orgs_header = ["OrganizationName", "OrganizationType", "OrganizationWebpage", "Description"]
    Sources_header = ['SourceName','SourceWebpage','SourceCitation','PersonName','PersonName','Description']
    Methods_header = ['MethodName','MethodWebpage','MethodCitation','MethodTypeCV','PersonName','DataQuality','Description']

    exportTemplate.exportOrganizations(pd.DataFrame([], columns=Orgs_header))
    exportTemplate.exportPeople(pd.DataFrame([], columns=People_headers))
    exportTemplate.exportSources(pd.DataFrame([], columns=Sources_header))
    exportTemplate.exportMethods(pd.DataFrame([], columns=Methods_header))


    exportTemplate.exportResourcesType(ResourceType_Top_df, ResourceType_Bottom_df)
    Attribute_Frame_df=pd.DataFrame(Attributes_data_result, columns=columns_Attributes)
    exportTemplate.exportAttributes(Attribute_Frame_df)
    # -----------------------------------------


    Resource_data_result=conn.call('get_all_resource_data',{'network_id':Selected_network_id, 'scenario_id': Selected_scenario_id, 'include_values':'Y','include_metadata':'Y'} )
    Resource_data_result_df=json_normalize(Resource_data_result)



    Network_headers=['MasterNetworkName','ResourceTypeAcronym','SpatialReferenceNameCV','ElevationDatumCV','Description']

    ScenarioHeaders=['ScenarioName','MasterNetworkName','SourceName','MethodName','ScenarioStartDate',
                     'ScenarioEndDate',   'TimeStep','TimeStepUnitCV','Description']

   # master network sheet

    Network = conn.call('get_network',
                        {'network_id': Selected_network_id, 'scenario_id': Selected_scenario_id, 'include_values': 'N',
                         'summary': 'Y'})

    MasterNetworkName = Network['name']
    ResourceTypeAcronym = DatasetAcronym
    SpatialReferenceNameCV='WGS84' # leave it empty for now like the the next two too
    ElevationDatumCV='MSL'
    Description=''

    MasterNetwork_sheet_result = [[MasterNetworkName, ResourceTypeAcronym, SpatialReferenceNameCV, ElevationDatumCV, Description]]
    MasterNetwork_Frame_result = pd.DataFrame(MasterNetwork_sheet_result, columns=Network_headers)

    # scenario sheet
    Scenario_sheet_result = []

    try:
        ScenarioStartDate= datetime.strptime(Scenario['start_time'].split(' ')[0], '%Y-%m-%d').strftime("%m/%d/%Y")
    except:
        ScenarioStartDate = ''
    try:
        ScenarioEndDate=datetime.strptime(Scenario['end_time'].split(' ')[0], '%Y-%m-%d').strftime("%m/%d/%Y")
    except:
        ScenarioEndDate = ''
    try:
        TimeStep=Scenario['time_step']
    except:
        TimeStep = ''
    TimeStepUnitCV='' # empty
    try:
        Description=Scenario['description']
    except:
        Description = ''
    Scenario_sheet_result = [[ScenarioName, MasterNetworkName, SourceName, MethodName, ScenarioStartDate, ScenarioEndDate,
                             TimeStep, TimeStepUnitCV, Description]]
    Scenario_Frame_result = pd.DataFrame(Scenario_sheet_result, columns=ScenarioHeaders)

    exportTemplate.exportMasterNetwork(MasterNetwork_Frame_result)
    exportTemplate.exportScenario(Scenario_Frame_result)

    FreeText_data_result = []
    FreeText_data_header = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName']

    TimeSeriesValues_header= ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName']

    Timseries_header=['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName', 'MethodName','YearType',
                      'AggregationStatisticCV','AggregationInterval','IntervalTimeUnit','IsRegular','NoDataValue','Description']

    Seasonal_header= ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName','SourceName','MethodName']

    NumericValue_data_result = []
    TimeSeriesValues_data_result = []
    TimeSeries_data_result = []
    array_data_result = []

    SeasonalValues=[]


    ObjectType_lst={}

    columns_node_data = ['ObjectType', 'InstanceName', 'InstanceNameCV', 'ScenarioName', 'SourceName', 'MethodName',
                        'InstanceCategory', 'Longitude_x', 'Latitude_y', 'Description']
    Node_data_result = []
    node_names = {}


    for key in Network.keys():
        if key=='nodes':
            Nodes=Network[key]

            for node in Nodes:
                ObjectType=node['types'][0]['name']
                InstanceName=node['name']
                ObjectTyplology='NODE'
                ObjectType_lst[(InstanceName,ObjectTyplology)] = ObjectType  # Add "ObjectTyplology"


                NodeID=node['id']
                node_names[NodeID] = InstanceName
                Description=node['description']
                Longitude_x=node['x']
                Latitude_y=node['y']

                node_row = []
                for header in columns_node_data:
                    if header == 'ObjectType':
                        node_row.append(ObjectType)
                    elif header == 'InstanceName':
                        node_row.append(InstanceName)
                    elif header == 'Longitude_x':
                        node_row.append(Longitude_x)
                    elif header == 'Latitude_y':
                        node_row.append(Latitude_y)
                    elif header == 'Description':
                        node_row.append(Description)
                    elif header == 'ScenarioName':
                        node_row.append(ScenarioName)
                    elif header == 'SourceName':
                        node_row.append(SourceName)
                    elif header == 'MethodName':
                        node_row.append(MethodName)
                    else:
                        node_row.append('')

                Node_data_result.append(node_row)
    NodesData_df=pd.DataFrame(Node_data_result, columns=columns_node_data)
    exportTemplate.exportNodes(NodesData_df)

    columns_link_data = ['ObjectType', 'LinkInstanceName', 'InstanceNameCV', 'ScenarioName', 'SourceName', 'MethodName',
                        'StartNodeInstanceName', 'EndNodeInstanceName', 'InstanceCategory', 'Description']

    Link_data_result = []

    for key in Network.keys():
        if key == 'links':
            Links = Network[key]
            for link in Links:
                ObjectType= link['types'][0]['name']
                LinkInstanceName = link['name']
                ObjectTyplology='LINK'
                ObjectType_lst[(LinkInstanceName,ObjectTyplology)] = ObjectType  # # Add "Link"
                Description = link['description']
                StartNodeInstanceName = node_names[link['node_1_id']]
                EndNodeInstanceName = node_names[link['node_2_id']]

                link_row = []
                for header in columns_link_data:
                    if header == 'ObjectType':
                        link_row.append(ObjectType)
                    elif header == 'LinkInstanceName':
                        link_row.append(LinkInstanceName)
                    elif header == 'StartNodeInstanceName':
                        link_row.append(StartNodeInstanceName)
                    elif header == 'EndNodeInstanceName':
                        link_row.append(EndNodeInstanceName)
                    elif header == 'Description':
                        link_row.append(Description)
                    elif header == 'ScenarioName':
                        link_row.append(ScenarioName)
                    elif header == 'SourceName':
                        link_row.append(SourceName)
                    elif header == 'MethodName':
                        link_row.append(MethodName)
                    else:
                        link_row.append('')
                Link_data_result.append(link_row)


        if key == 'types':
            GlobalInstanceName = Network['name']
            ObjectType = Network['types'][0]['name']
            ObjectTyplology = 'NETWORK'

            #
            #
            # ResourceTypeAcronym + ' Global Attributes'
            ObjectType_lst[(GlobalInstanceName,ObjectTyplology)] = ObjectType # Add "Network"


    LinksData_df = pd.DataFrame(Link_data_result, columns=columns_link_data)
    exportTemplate.exportLinkes(LinksData_df)

    YearType='CalenderYear'
    AggregationStatisticCV='Average'
    AggregationInterval='1'
    IntervalTimeUnit='month'
    IsRegular=''
    NoDataValue='-9999'
    Description=''

    for index, row in Resource_data_result_df.iterrows():
        ObjectTyplology=row['ref_key']
        InstanceName = row['ref_name']
        ObjectType = ''




        if (InstanceName, ObjectTyplology) in ObjectType_lst.keys():  # here we need to also use "Node" or "Link" or "Network" in addition to Instance Name
            # Look up the ObjectType in the NodesData_df using the InstanceName
            ObjectType= ObjectType_lst[(InstanceName,ObjectTyplology)]

            # check if the attribute does not exist for this Object Type in the Attributes table.
            # if it does not exist then continie the for loop (to skip the rest of he code)
            AttributeName = row['attr_name']
            exist_row = Attribute_Frame_df[(Attribute_Frame_df.ObjectType == ObjectType) & (Attribute_Frame_df.AttributeName == AttributeName)]
            if exist_row.empty:
                continue

        # get metadata
        dataset_metadata = json.loads(row['dataset_metadata'])

        if not 'source' in  dataset_metadata.keys():
            SourceName='AddSource'
        else:
            SourceName=dataset_metadata['source']

        if not 'method' in  dataset_metadata.keys():
            MethodName='AddMethod'
        else:
            MethodName=dataset_metadata['method']

        # ValuesSheets['ScenarioName']=row['ref_name']

        # AttributeName = row['attr_name']

        # leave the  object type, method, and source, scenario, columns empty for now.ps

        if row['dataset_type']=='descriptor':
            FreeText_value = row['dataset_value']
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
            NumericValue_value=row['dataset_value']
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
            NumericValue_data_result.append(output_row)


        if row['dataset_type']=='timeseries':
            json_times = json.loads(row['dataset_value'])
            for key in json_times.keys():
                if key == 'Header' :  continue
                all_monthes = {}
                for time in json_times[key].keys():
                    value = json_times[key][time]
                    output_row = []
                    output_row_times = []
                    year = time.split('T')[0]
                    if not '9998' in year and not '9999' in year:  # these years indicate sesonal data
                        for header in TimeSeriesValues_header:
                            if header == "InstanceName":
                                output_row.append(InstanceName)
                            elif header == "ObjectType":
                                output_row.append(ObjectType)
                            elif header == "AttributeName":
                                output_row.append(AttributeName)
                            elif header == 'ScenarioName':
                                output_row.append(ScenarioName)
                            else:
                                output_row.append('')
                        output_row.append(datetime.strptime(time.split('T')[0], '%Y-%m-%d').strftime("%Y/%m/%d")) ### format MM/DD/YYYY  1975-12-01T00:00:00.000000000Z
                        if value == '':
                            value = '-9999'
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

                        # Timseries_header = ['ObjectType', 'InstanceName', 'ScenarioName', 'AttributeName', 'SourceName',
                        #                     'MethodName', 'YearType',
                        #                     'AggregationStatisticCV', 'AggregationInterval', 'IntervalTimeUnit',
                        #                     'IsRegular', 'NoDataValue', 'Description']
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
                            SeasonName = 'Nov'
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


                        output_row.append(SeasonName)
                        output_row.append(SeasonNameCV)
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
                    except:
                        value = ''
                    output_row.append(value)
                array_data_result.append(output_row)



    FreeText_data_header.append('FreeText') # it shows "numeric" in the last column but should be FreeText

    FreeText_frame_result = pd.DataFrame(FreeText_data_result, columns=FreeText_data_header)


    # Attribute_Frame_df
    # Drop the rows if they contain an attribute that does not exist in the template for the same ObjecType

    # FreeText_frame_result_df = FreeText_frame_result[FreeText_frame_result.AttributeName != 0]

    exportTemplate.exportFreeText(FreeText_frame_result)

    FreeText_data_header.pop(-1)

    FreeText_data_header.append('NumericValue') # this one should be for Numric not
    NumericValue_frame_result = pd.DataFrame(NumericValue_data_result, columns=FreeText_data_header)

    # Attribute_Frame_df
    # Drop the rows if they contain an attribute that does not exist in the template for the same ObjecType

    # NumericValue_frame_result_df = NumericValue_frame_result[NumericValue_frame_result.AttributeName != 0]

    exportTemplate.exportNumericValue(NumericValue_frame_result)

    TimeSeriesValues_header.append('DateTimeStamp')
    TimeSeriesValues_header.append('Value')
    TimeSeriesValues_frame_result = pd.DataFrame(TimeSeriesValues_data_result, columns=TimeSeriesValues_header)

    TimeSeriesValues_frame_result=TimeSeriesValues_frame_result.sort_values(['ObjectType', 'InstanceName', 'ScenarioName',
                                                                            'AttributeName', 'DateTimeStamp'])
    TimeSeriesValues_frame_result['DateTimeStamp'] = pd.to_datetime(TimeSeriesValues_frame_result.DateTimeStamp).apply(lambda x:x.strftime('%m/%d/%Y'))

    # Here, lets get the unique rows based on the ObjectType', 'InstanceName', 'ScenarioName',  AttributeName
    Times_frame_result = pd.DataFrame(TimeSeries_data_result, columns=Timseries_header)
    Times_frame_result=Times_frame_result.drop_duplicates()
    exportTemplate.exportTimeSeries(Times_frame_result)

    exportTemplate.exportTimeSeriesValues(TimeSeriesValues_frame_result)



    Seasonal_header.append('SeasonName')
    Seasonal_header.append('SeasonNameCV')
    Seasonal_header.append('SeasonValue')
    SeasonalValues_df = pd.DataFrame(SeasonalValues, columns=Seasonal_header)
    exportTemplate.exportSeasonal(SeasonalValues_df)



    FreeText_data_header.pop(-1)
    for i in range(1, 7):
        header_name = 'AttributeName{}_Values'.format(i)
        FreeText_data_header.append(header_name)
    array_frame_result = pd.DataFrame(array_data_result, columns=FreeText_data_header)
    muti_header = ['MultiAttributeSeriesName',	'AttributeName1',	'AttributeName2',	'AttributeName3',	'AttributeName4',	'AttributeName_Column5',	'AttributeName_Column6']
    up_frame_data = pd.DataFrame([], columns=muti_header)
    exportTemplate.exportMulti(up_frame_data, array_frame_result)

    header_node_data = ['ObjectType', 'InstanceName', 'InstanceNameCV', 'ScenarioName', 'SourceName', 'MethodName',
                        'InstanceCategory', 'Longitude_x', 'Latitude_y', 'Description']


    header_link_data = ['ObjectType', 'InstanceName', 'InstanceNameCV', 'ScenarioName', 'SourceName', 'MethodName',
                        'StartNodeInstanceName', 'EndNodeInstanceName', 'InstanceCategory', 'Description']



    print 'Done'




