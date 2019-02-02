
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
login_response = conn.login('amabdallah@aggiemail.usu.edu', 'pass')


Parent_Resource_data_result = conn.call('get_all_resource_data',
                                       {'network_id': 1122, 'scenario_id': 2377,
                                        'include_values': 'Y', 'include_metadata': 'Y'})
Parent_Resource_data_result_df = json_normalize(Parent_Resource_data_result)
