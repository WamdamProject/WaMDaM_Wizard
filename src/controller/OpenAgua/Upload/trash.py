

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
login_response = conn.login('amabdallah@aggiemail.usu.edu', 'OApass!')

# get_all_dimensions = conn.call('get_all_dimensions', ({}))


# add_scen = conn.call('add_scenario', {'network_id': 1076, 'scen': {'name': 'test2',
#                                                                    'description': 'This scenario is for calibration',
#                                                                    'id': None,
#                                                                     'network_id': 1076,
#                                                                    'start_time': '1990-01-01T00:00:00',
#                                                                    'layout.class': u'scenarios',
#                                                                    'resourcescenarios': [],
#                                                                    'end_time': '2014-12-31T00:00:00',
#                                                                    'time_step': 'month',
#                                                                    }})
#
# Get_scenarios_metadata = conn.call('get_scenarios',
#                                    {'network_id': 1863, 'include_values': 'N'})
# Get_scenarios_metadata_df = json_normalize(Get_scenarios_metadata)
#
# result_scenario = conn.call('update_scenario',
#                                              {'network_id': 1090, 'scen': {
#                                                  'id': 2328,
#                                                 'network_id': 1090,
#                                                  'name': '',
#                                                  # 'description': 'This scenario is for calibration. It can be used to test variables before saving them to Baseline.',
#                                                  'layout': {
#                                                      'class': 'scenario',
#                                                      'parent': 2327
#                                                             }
#                                                                             }
#                                               }
#                             )

# add_scen = conn.call('add_scenario', {'network_id': 1086, 'scen': {'name': u'Calibration2',
#                                                                    'description': 'This scenario is for calibration. It can be used to test variables before saving them to Baseline.',
#                                                                    'id': None,
#                                                                    'start_time': '1990-01-01T00:00:00',
#                                                                    'layout.class': u'results',
#                                                                    'resourcescenarios': [],
#                                                                    'end_time': '2014-12-31T00:00:00',
#                                                                    'time_step': 'month',
#                                                                    }})



result='update_scenario', {'network_id': 1444, 'scen': {'layout': {'class': u'scenario'},
                                                         'description': u'Scenario',
                                                         'network_id': 1444, 'parent_id': 3433,
                                                         'id': 3434, 'name': u'Reuso Industrial'}}