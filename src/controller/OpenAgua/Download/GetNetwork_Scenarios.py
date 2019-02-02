# Get the network, scenarios, and the nodes and links

from pandas.io.json import json_normalize
import pandas as pd
from datetime import datetime

def GetNetworkScenarios(conn, Selected_network_id, Selected_scenario_id, DatasetAcronym):
    MethodName = 'AddMethodName'
    SourceName = 'AddSourceName'


    Network_headers = ['MasterNetworkName', 'ResourceTypeAcronym', 'SpatialReferenceNameCV', 'ElevationDatumCV',
                       'Description']

    ScenarioHeaders = ['ScenarioName', 'MasterNetworkName', 'SourceName', 'MethodName', 'ScenarioStartDate',
                       'ScenarioEndDate', 'TimeStep', 'TimeStepUnitCV', 'ScenarioParentName','ScenrioType','Description']


    # master network sheet

    Network = conn.call('get_network',
                        {'network_id': Selected_network_id, 'scenario_id': Selected_scenario_id, 'include_values': 'N',
                         'summary': 'Y'})

    MasterNetworkName = Network['name']
    ResourceTypeAcronym = DatasetAcronym
    SpatialReferenceNameCV = 'WGS84'  # leave it empty for now like the the next two too
    ElevationDatumCV = 'MSL'
    Description = ''

    MasterNetwork_sheet_result = [
        [MasterNetworkName, ResourceTypeAcronym, SpatialReferenceNameCV, ElevationDatumCV, Description]]
    MasterNetwork_Frame_result = pd.DataFrame(MasterNetwork_sheet_result, columns=Network_headers)

    # scenario sheet
    Scenario_sheet_result = []

    # ChildScenarioID
    #
    # Look it up here


    # Scenario=conn.call('get_scenario',{'scenario_id': Selected_scenario_id})
    # ScenarioName=Scenario['name']

    # Selected_scenario_id is the parent ID

    Get_scenarios_metadata = conn.call('get_scenarios',
                                       {'network_id': Selected_network_id, 'include_values': 'N'})
    Get_scenarios_metadata_df = json_normalize(Get_scenarios_metadata)

    # Look up the parent scenario
    # Children={}
    ParentScenario = []
    ParentScenario_ID = []

    #
    Selected_scenario_ids = []

    ScenarioName = []
    ScenarioStartDate = []
    ScenarioEndDate = []
    TimeStepUnitCV = []
    Description = []
    ScenrioType=[]
    TimeStep = []
    ObjectType_lst = {}
    ScenarioParentName=[]
    Node_data_result = []
    Link_data_result = []
    node_names = {}
    SeasonalValues = []


    columns_node_data = ['ObjectType', 'InstanceName', 'InstanceNameCV', 'ScenarioName', 'SourceName', 'MethodName',
                         'InstanceCategory', 'Longitude_x', 'Latitude_y', 'Description']

    columns_link_data = ['ObjectType', 'LinkInstanceName', 'InstanceNameCV', 'ScenarioName', 'SourceName', 'MethodName',
                         'StartNodeInstanceName', 'EndNodeInstanceName', 'InstanceCategory', 'Description']

    for row1 in Get_scenarios_metadata_df.iterrows():
        if row1[1]['layout.class'] == 'baseline':
            # use the select scenario id to look up the children
            try:
                Children_Ids = row1[1]['layout.children']
            except:
                Children_Ids=[]

    Selected_scenario_ids.append(Selected_scenario_id)
    for Children_Id in Children_Ids:
        Selected_scenario_ids.append(Children_Id)

    for row in Get_scenarios_metadata_df.iterrows():
        if row[0] == 0:
            # only for the first row.
            ParentScenarioStartDate = datetime.strptime(row[1]['start_time'].split(' ')[0], '%Y-%m-%d').strftime("%m/%d/%Y")
            ParentScenarioEndDate = datetime.strptime(row[1]['end_time'].split(' ')[0], '%Y-%m-%d').strftime("%m/%d/%Y")
            ParentTimeStepUnitCV = row[1]['time_step']
        # reset  Selected_scenario_id
        Selected_scenario_id = []

        scenario_flag = False
        for Selected_scenario_id in Selected_scenario_ids:
            # only the parent and its children. Ignore other scenarios that neither parent nor children
            if Selected_scenario_id == row[1]['id']:
                ScenarioName = row[1]['name']
                # print ScenarioName

                try:
                    ScenarioStartDate = datetime.strptime(row['start_time'].split(' ')[0], '%Y-%m-%d').strftime("%m/%d/%Y")
                except:
                    ScenarioStartDate = ParentScenarioStartDate  # use the parent ScenarioStartDate value
                try:
                    ScenarioEndDate = datetime.strptime(row['end_time'].split(' ')[0], '%Y-%m-%d').strftime("%m/%d/%Y")
                except:
                    ScenarioEndDate = ParentScenarioEndDate  # use the parent ScenarioEndDate value

                TimeStep = 1

                # if it does not exist (e.g., , then use the parent value
                try:
                    if str(row[1]['time_step']) != 'nan':
                        TimeStepUnitCV = row[1]['time_step']
                    else:
                        TimeStepUnitCV = ParentTimeStepUnitCV
                # in case ['time_step'] does not exist in the child scenario

                except:
                    TimeStepUnitCV = ParentTimeStepUnitCV


                try:
                    ScenarioParentID = row[1]['layout.parent']
                    if ScenarioParentID:
                        Scenario = conn.call('get_scenario', {'scenario_id': ScenarioParentID})
                        ScenarioParentName = Scenario['name']
                    else:
                        ScenarioParentName='self'

                except:
                    ScenarioParentName = 'self'

                try:
                    ScenrioType = row[1]['layout.class']  # values as: baseline, scenario, results
                except:
                    ScenrioType = ''

                try:
                    Description = row[1]['description']
                except:
                    Description = ''


                scenario_flag = True
                break

        if scenario_flag:
            Scenario_sheet_result.append(
                [ScenarioName, MasterNetworkName, SourceName, MethodName, ScenarioStartDate, ScenarioEndDate,
                 TimeStep, TimeStepUnitCV, ScenarioParentName,ScenrioType,Description])






    # for row in Get_scenarios_metadata_df.iterrows():
    #
    #     for Selected_scenario_id in Selected_scenario_ids:
    #         # only the parent and its children. Ignore other scenarios that neither parent nor children
    #         if Selected_scenario_id == row[1]['id']:
    #             ScenarioName = row[1]['name']

            for key in Network.keys():
                if key == 'nodes':
                    Nodes = Network[key]

                    for node in Nodes:
                        ObjectType = node['types'][0]['name']
                        InstanceName = node['name']
                        ObjectTyplology = 'NODE'
                        ObjectType_lst[(InstanceName, ObjectTyplology)] = ObjectType

                        NodeID = node['id']
                        node_names[NodeID] = InstanceName
                        Description = node['description']
                        Longitude_x = node['x']
                        Latitude_y = node['y']

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
            # Node_data_result_all.extend(Node_data_result)

            # Link_data_result = []

            for key in Network.keys():
                if key == 'links':
                    Links = Network[key]
                    for link in Links:
                        ObjectType = link['types'][0]['name']
                        LinkInstanceName = link['name']
                        ObjectTyplology = 'LINK'
                        ObjectType_lst[(LinkInstanceName, ObjectTyplology)] = ObjectType  # # Add "Link"
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

                # Network object
                if key == 'types':
                    GlobalInstanceName = Network['name']
                    ObjectType = Network['types'][0]['name']
                    ObjectTyplology = 'NETWORK'
                    ObjectType_lst[(GlobalInstanceName, ObjectTyplology)] = ObjectType  # Add "Network"

                # Link_data_result_all.extend(Link_data_result)


    Scenario_Frame_result = pd.DataFrame(Scenario_sheet_result, columns=ScenarioHeaders)
    LinksData_df = pd.DataFrame(Link_data_result, columns=columns_link_data)

    NodesData_df = pd.DataFrame(Node_data_result, columns=columns_node_data)

    return MasterNetwork_Frame_result,Scenario_Frame_result,NodesData_df,LinksData_df,\
           Selected_scenario_ids,ObjectType_lst
