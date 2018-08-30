

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
login_response = conn.login('amabdallah@aggiemail.usu.edu', 'xxxxxx')


# url = "http://server.basinit.hydra.org.uk/"
# conn = JsonConnection(url)
# login_response = conn.login('amabdallah@aggiemail.usu.edu', 'Hydra2017')


all_attributes = conn.call('get_all_attributes', ({}))

# print all_attributes
#
# for attr in all_attributes:
#     attributes[attr.id] = attr.name
#
#
network_id=5
network = conn.call('get_network', {'network_id': network_id})
print network