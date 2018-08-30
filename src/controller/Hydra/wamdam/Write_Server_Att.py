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
import csv

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
login_response = conn.login('amabdallah@aggiemail.usu.edu', 'xxxxxxxxxxxx!')



# get_templates()
all_templates = conn.call('get_templates', ({}))
# print all_templates


# get all Attributes on the server
all_attributes = conn.call('get_all_attributes', ({}))
# all_attr_dict = {}
# for a in all_attributes:
#     all_attr_dict[a.name] = {'id': a.id, 'dimension': a.dimen}



def write_dict_data_to_csv_file(csv_file_path, dict_data):
    # print all_templates

    csv_file = open(csv_file_path, 'wb')
    writer = csv.writer(csv_file, dialect='excel')

    headers = dict_data[0].keys()
    writer.writerow(headers)

    for dat in dict_data:
        line = []
        for field in headers:
            line.append(dat[field])
        writer.writerow(line)

    csv_file.close()

print 'Saved Server_templets.csv'


write_dict_data_to_csv_file('Server_templets.csv', all_templates)



def write_dict_data_to_csv_file(csv_file_path, dict_data):
    # print all_templates

    csv_file = open(csv_file_path, 'wb')
    writer = csv.writer(csv_file, dialect='excel')

    headers = dict_data[0].keys()
    writer.writerow(headers)

    for dat in dict_data:
        line = []
        for field in headers:
            line.append(dat[field])
        writer.writerow(line)

    csv_file.close()
print 'Saved Server_attrs.csv'




write_dict_data_to_csv_file('Server_attrs.csv', all_attributes)