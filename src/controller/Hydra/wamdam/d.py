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
import os

# set the path to the Hydra repository to import its libraries
import sys
sys.path.append("C:\Users\Adel\Documents\GitHub\HydraPlatform\HydraServer\HydraLib\python")

import argparse as ap

# Python utility libraries.
from HydraLib.HydraException import HydraPluginError
from HydraLib.PluginLib import JsonConnection, \
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
url = "http://server.test.hydra.org.uk/"
conn = JsonConnection(url)
# # connects by default to 'localhost:8080'
conn.login("amabdallah@aggiemail.usu.edu", "Hydra2017")


#url = "http://localhost:8080/"
#conn = JsonConnection(url)
# connects by default to 'localhost:8080'
#conn.login("root", "")



# Use the 'get_projects' call to check for an existing project of this name by listing all available projects.
# The project concept does not exist in WaMDaM but it is needed in Hydra. We define it here
projects = conn.call('get_projects', {})
print projects
all_attributes = conn.call('get_all_attributes', ({}))

print all_attributes

tempDB = conn.call('get_templates', {})


print tempDB

