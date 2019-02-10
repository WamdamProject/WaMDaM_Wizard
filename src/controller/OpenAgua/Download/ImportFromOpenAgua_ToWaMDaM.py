

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

    # hard coded metadata can be upated here. Right now, they dont exist in Hydra/OpenAgua for nodes and links.
    # future work will allow a systematic way to define these metadata items in Hydra which then allows us to import them back to WaMDaM

    MethodName='AddMethodName'
    SourceName='AddSourceName'

    exportTemplate = ExportTemplate(ExportFilePath)


    Template=conn.call('get_template',{'template_id':Selected_template_id})


    EndTime=''
    # -----------------------------------------
    columns_ResourceType=['ResourceType',	'ResourceTypeAcronym','MethodName','Description']

    columns_ObjecTypes = ['ObjectType','ObjectTypology','DatasetAcronym','ObjectTypeCV','Layout','ObjectCategory','Description']


    columns_Attributes = ['ObjectType','AttributeName','AttributeName_Abstract','AttributeNameCV','AttributeUnit','AttributeUnitCV',
                          'AttributeDataTypeCV','AttributeCategory','ModelInputOrOutput','AttributeDescription','AttributeScale']#,'AttributeID']
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
                            # AttributeID=attr['attr_id']


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
                                # elif 'AttributeID' == header:
                                #     attribute_row.append(AttributeID)
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


    from controller.OpenAgua.Download.GetNetwork_Scenarios import GetNetworkScenarios

    MasterNetwork_Frame_result, Scenario_Frame_result,\
    NodesData_df, LinksData_df,\
    Selected_scenario_ids,ObjectType_lst=GetNetworkScenarios(conn, Selected_network_id, Selected_scenario_id, DatasetAcronym)

    exportTemplate.exportMasterNetwork(MasterNetwork_Frame_result)
    exportTemplate.exportScenario(Scenario_Frame_result)
    exportTemplate.exportNodes(NodesData_df)
    exportTemplate.exportLinkes(LinksData_df)

    #########################################################################################################################################3

    # loop through the scenarios (if more than one is available)
    # first get the Parent Scenario and get its data and process it below
    # second, loop though the child scenarios and if they have data, overwrite the parent data
    # append the data for all the scenarios together and print them one time to the sheets

    ##################################################################################################################
    # Get and process scenario data
    ##################################################################################################################
    # reset the scenario ID to pass it with its children as well
    Selected_scenario_id=[]

    from controller.OpenAgua.Download.GetScenarioData import   GetScenarioData

    FreeText_frame_result, NumericValue_frame_result, SeasonalValues_df, \
    Times_frame_result, TimeSeriesValues_frame_result,\
    up_frame_data, array_frame_result=GetScenarioData(Selected_scenario_ids,conn,Selected_network_id,Attribute_Frame_df,ObjectType_lst)


    exportTemplate.exportFreeText(FreeText_frame_result)


    exportTemplate.exportNumericValue(NumericValue_frame_result)

    exportTemplate.exportTimeSeries(Times_frame_result)

    exportTemplate.exportTimeSeriesValues(TimeSeriesValues_frame_result)


    exportTemplate.exportSeasonal(SeasonalValues_df)


    exportTemplate.exportMulti(up_frame_data, array_frame_result)


    print 'Done'




