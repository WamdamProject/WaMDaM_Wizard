import json
from pandas.io.json import json_normalize
import pandas as pd
import os, csv
import sqlite3
from json import loads
from collections import OrderedDict
# set the path to the Hydra repository to import its libraries
# import sys
# sys.path.append("C:\Users\Adel\Documents\GitHub\HydraPlatform\HydraServer\HydraLib\python")

import argparse as ap

# Python utility libraries.
from controller.OpenAgua.HydraLib.HydraException import HydraPluginError

# Import Scenario from WaMDaM SQLite using the API
from controller.wamdamAPI.GetResourceStructure import GetResourceStructure
from controller.wamdamAPI.GetMetadataByScenario import GetMetadataByScenario

from controller.wamdamAPI.GetInstancesByScenario import GetInstancesBySenario
from controller.wamdamAPI.GetAllValuesByScenario import GetAllValuesByScenario
from controller.wamdamAPI.GetUnitCVs import GetUnits

from controller.OpenAgua.HydraLib.PluginLib import JsonConnection, \
    create_xml_response, \
    write_progress, \
    write_output

# General library for working with JSON objects
import json
# Used for working with files.
import os, sys, datetime

import logging

ur = "https://data.openagua.org"
conn = JsonConnection(ur)
login_response = conn.login('amabdallah@aggiemail.usu.edu', 'TestOpenAgua!')

projectID=1916
selectedMasterNetworkName='Qatar Mega Reservoirs'

GetNetworks_metadata = conn.call('get_networks', {'project_id': projectID, 'include_values': 'N'})
GetNetworks_metadata_df = json_normalize(GetNetworks_metadata)


# for network_row in GetNetworks_metadata_df.iterrows():
#     if network_row[1]['name'] == selectedMasterNetworkName:
#         network_id = network_row[1]['id']



# Get all the scenarios inside the uploaded network
Get_scenarios_metadata = conn.call('get_scenarios',
                                   {'network_id': 1138, 'include_values': 'N'})

Get_scenarios_metadata_df = json_normalize(Get_scenarios_metadata)

print 'x'

result_scenario = conn.call('update_scenario',
                                        {'network_id': 1138, 'scen': {
                                            'id': 2424,
                                            'network_id': 1138,
                                            'name': 'Cons25PercCacheUrbWaterUse_result',
                                            # 'description': 'This scenario is for calibration. It can be used to test variables before saving them to Baseline.',
                                            'layout': {
                                                'class': 'results',
                                                'parent': 2422
                                            }
                                            }
                                             }
                                            )






# Use the scenario name to look up its ID
#
# for i in range(len(scenario_sheet)):
#     for row in Get_scenarios_metadata_df.iterrows():
#         ScenarioName = scenario_sheet.values[i][0]
#         ScenarioParentName = scenario_sheet.values[i][8]
#         if ScenarioParentName == 'self' or ScenarioParentName == 'Self':
#             if ScenarioNam e== row[1]['name']: # matching the spreadsheet with the online uploaded scenario
#                 ScenarioParentI D =row[1]['id']
#                 break
#             break
#
#
#         else:
#             if ScenarioNam e== row[1]['name']: # matching the spreadsheet with the online uploaded scenario
#                 ScenarioParentI D =row[1]['id']
#                 ChildScenarioI D =ScenarioParentI D =row[1]['id']
#                 result_scenario = conn.call('update_scenario',
#                                             {'network_id': network_id, 'scen': {
#                                                 'id': ChildScenarioID,
#                                                 'network_id': network_id,
#                                                 'name': '',
#                                                 # 'description': 'This scenario is for calibration. It can be used to test variables before saving them to Baseline.',
#                                                 'layout': {
#                                                     'class': 'scenario',
#                                                     'parent': ScenarioParentID
#                                                 }
#                                             }
#                                              }
#                                             )
#
# #
#

