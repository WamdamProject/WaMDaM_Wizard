# coding: utf-8


# This file builds a hydra template from the wamdam workbook.
# The file intends to export WaMDaM data that exist in the workbook
# into Hydra database

# The file reads WaMDaM workbook, then it maps each table in WaMDaM into the Hydra web-service
# Hydra API: http://umwrg.github.io/HydraPlatform/devdocs/HydraServer/index.html#api-functions

# steps
# Step 1: connect to the Hydra server
# Step 2: Import the WaMDaM workbook sheets
# Step 3: Define a project in Hydra. Add the template "dataset name", Object Types and Attribuets in Hydra
# Step 4: Import WaMDaM Network, Nodes, and links
# Step 5: Import Scenarios and Data Values of Attributes for Nodes and links



import pandas as pd
import os, csv
from json import loads
from collections import OrderedDict
# set the path to the Hydra repository to import its libraries
# import sys
# sys.path.append("C:\Users\Adel\Documents\GitHub\HydraPlatform\HydraServer\HydraLib\python")

import argparse as ap

# Python utility libraries.

from controller.Hydra.HydraLib.HydraException import HydraPluginError
from controller.Hydra.HydraLib.PluginLib import JsonConnection, \
    create_xml_response, \
    write_progress, \
    write_output

# General library for working with JSON objects
import json
# Used for working with files.
import os, sys, datetime

import logging

log = logging.getLogger(__name__)

# STEP 1: connect to the Hydra server
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Connect to the Hydra server on the local machine
# More info: http://umwrg.github.io/HydraPlatform/tutorials/plug-in/tutorial_json.html#creating-a-client
# url = "http://127.0.0.1:8080"
# conn = JsonConnection(url)
# # connects by default to 'localhost:8080'
# conn.login("root", "")

# Connect to the Hydra server on the local machine
# More info: http://umwrg.github.io/HydraPlatform/tutorials/plug-in/tutorial_json.html#creating-a-client
ur = "https://data.openagua.org"
conn = JsonConnection(ur)
login_response = conn.login('amabdallah@aggiemail.usu.edu', 'TestOpenAgua!')


# Add units and their dim. Look up all the excel sheet, find the units and their dim
unites = []
dimensions = []
Sever_dimensions=conn.call('get_dimensions', {})
all_attributes = conn.call('get_all_attributes', ({}))

get_all_dimensions=conn.call('get_all_dimensions', ({}))



# Print all units in the server into csv
Sever_dimensions=get_all_dimensions
file_units = open("Server_units.csv","wb")
writer = csv.writer(file_units, delimiter=',',quoting=csv.QUOTE_ALL)
units_fields = ['name', 'abbr', 'lf', 'dimension', 'info']
writer.writerow(units_fields)

for ServerDim in Sever_dimensions:
    if 'unknown' in str(ServerDim['name'].lower()) or 'dimensionless' in str(ServerDim['name']):
        continue
    print ServerDim['name']
    Units = conn.call('get_units', {'dimension': ServerDim['name']})

    for unit in Units:
        unit_values = OrderedDict()
        for key in units_fields:
            if key in unit.keys():
                if isinstance(unit[key], unicode):
                    unit_values[key] = unit[key].encode('utf-8')
                else:
                    unit_values[key] = unit[key]
            else:
                unit_values[key] = None
        writer.writerow(unit_values.values())


# for j in range(len(attr_sheet)):
#     if j < 9: continue # avoid headers in excel
#     attr_unit = attr_sheet.values[j][3].strip() # Attribute unit name in Excel
#     attr_dimension = attr_sheet.values[j][5].strip() # UnitType in excel
#     if not attr_dimension in Sever_dimensions:
#         result = conn.call('add_dimension', {'dimension': attr_dimension})
#         dimensions.append(attr_dimension)
#
#     result_get = conn.call('get_units', {'dimension': attr_dimension})
#     # print result_get
#
#     is_unit_exist = False
#     for unit in result_get:
#         if attr_unit == unit['name']:
#             is_unit_exist = True
#             break
#
#     if not is_unit_exist:
#         unites.append(attr_unit)
#         new_unit = {'name': attr_unit, 'dimension': attr_dimension, 'abbr': attr_unit, 'lf': 1, 'cf': 0} #
#
#         # print new_unit
#         result_unit = conn.call('add_unit', {'unit': new_unit})
#         result_get = conn.call('get_units', {'dimension': attr_dimension})
#         # print result_get