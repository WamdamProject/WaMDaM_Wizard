
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

ur = "https://www.openagua.org/api/v1/hydra/"
conn = JsonConnection(ur)
login_response = conn.login('amabdallah@aggiemail.usu.edu', password)


Parent_Resource_data_result = conn.call('get_all_resource_data',
                                       {'network_id': 77, 'scenario_id': 75,
                                        'include_values': 'Y', 'include_metadata': 'Y'})
Parent_Resource_data_result_df = json_normalize(Parent_Resource_data_result)

# print Parent_Resource_data_result_df



Child_Resource_data_result = conn.call('get_all_resource_data',
                                       {'network_id': 77, 'scenario_id': 1512,
                                        'include_values': 'Y', 'include_metadata': 'Y'})
Child_Resource_data_result_df = json_normalize(Child_Resource_data_result)

# print Child_Resource_data_result_df



for index, row in Parent_Resource_data_result_df.iterrows():
    for index_child, row_child in Child_Resource_data_result_df.iterrows():

        if row['resource_attr_id'] == row_child['resource_attr_id']:
            if row['dataset_id'] != row_child['dataset_id']:
                print row['dataset_id']
            else:
                pass
            # all_diff = row_child.equals(row)
            # if not all_diff:
        #
