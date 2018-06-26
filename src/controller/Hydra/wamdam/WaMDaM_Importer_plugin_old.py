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
from json import loads

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
# url = "http://127.0.0.1:8080"
# conn = JsonConnection(url)
# connects by default to 'localhost:8080'
# conn.login("root", "")

# Connect to the Hydra server on the local machine
# More info: http://umwrg.github.io/HydraPlatform/tutorials/plug-in/tutorial_json.html#creating-a-client
url = "https://data.openagua.org"
conn = JsonConnection(url)
login_response = conn.login('amabdallah@aggiemail.usu.edu', 'TestOpenAgua!')


# url = "http://server.basinit.hydra.org.uk/"
# conn = JsonConnection(url)
# login_response = conn.login('amabdallah@aggiemail.usu.edu', 'Hydra2017')


all_attributes = conn.call('get_all_attributes', ({}))

get_all_dimensions=conn.call('get_all_dimensions', ({}))

# STEP 2: Import the WaMDaM workbook sheets
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# Load the excel file into pandas
wamdam_data = pd.read_excel('./Qatar.xlsm', sheetname=None)
# wamdam_data = pd.read_excel('./WEAP_test3.xlsm', sheetname=None)

# This returns an object, which is a dictionary of pandas 'dataframe'.
# The keys are sheet names and the dataframes are the sheets themselves.
wamdam_data.keys()

# Define the WaMDaM sheets to import
# Import the Datasets and Object Types
type_sheet = wamdam_data['2.1_Datasets&ObjectTypes']

# Import the attributes
attr_sheet = wamdam_data['2.2_Attributes']

# STEP 3: Define a project in Hydra. Add the template "dataset name", Object Types and Attributes in Hydra
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# Use the 'get_projects' call to check for an existing project of this name by listing all available projects.
# The project concept does not exist in WaMDaM but it is needed in Hydra. We define it here
projects = conn.call('get_projects', {})
proj_id = 1
proj_name = "WaMDaM_%s"
# Identify the highest project ID number.
for p in projects:
    if p.name.find('WaMDaM_') == 0:
        try:
            proj_id = int(p.name.replace('WaMDaM_', ''))
        except:
            continue
# Add 1 to the hightest proj numner
log.info(proj_id)
log.info(proj_name)
proj_id = proj_id + 1
## Load the Project name to the Hydra db
my_new_project = conn.call('add_project', {'project': {'name': proj_name % proj_id}})

# Add the attribute:
# Attributes in Hydra are independent of ObjectTypes or templates types (they can be shared across object types)

# Look all the unique attributes in 2.2_Attributes sheet.  Get the AttributeUnit for each attribute.

# The "UnitType" in WaMDaM is equivalent to "dimension" in Hydra
# my_new_attr_list = []
# my_new_attr = conn.call('add_attribute', {'attr': {'name': ['attr'], 'dimension': ['Volume']}})


all_attributes = conn.call('get_all_attributes', ({}))
all_attr_dict = {}
for a in all_attributes:
    all_attr_dict[a.name.lower()] = {'id': a.id, 'dimension': a.dimen}

# print all_attr_dict
# -------------------------

# Create a new template (dataset)
# This will fail second time around due to a unique naming restriction.
# You should call 'get_templates' first and update an existing one if one with the same name is already there.

# 2.1_Datasets&ObjectTypes sheet, look in the Datasets_table
# DatasetName which is cell A10 in 2.1_Datasets&ObjectTypes sheet

template = {'name': type_sheet.values[8][0], 'types': []}  # insert the value of the "DatasetName" from excel
# A template is equivalent to a dataset in wamdam

# my_templates lists available templates. A template equates to the 'Dataset' in WaMDaM.
# Go through this worksheet, building a hydra template
my_templates = conn.call('get_template_attributes', {})

# -----------------------------

# Go through the excel sheet and pull out the template type definitions...
# a template type in Hydra is equivalent to an Object Type in WaMDaM
# resource_type in Hydra is equivalent to an ObjectTypology in WaMDaM
# typeAttrs (the same as Template Type Attributes) links attributes to their template

# 2.1_Datasets&ObjectTypes sheet, look in the ObjectTypes_table

# iterate to get the object types and their attributes
# start reading from row 16 because value is staring from 16 row.
for i in range(len(type_sheet)):
    if type_sheet.values[i + 16][0] == "" or str(type_sheet.values[i + 16][0]) == "nan" :
        break
    #  type_sheet.values[i + 16][0]--ObjectType
    #  type_sheet.values[i + 16][1]--ObjectTypology

#  Based on the link below, add a layout =Icon
# http://umwrg.github.io/HydraPlatform/devdocs/HydraServer/index.html?highlight=typeattrs#HydraServer.soap_server.hydra_complexmodels.TemplateType

    # read value of layout from  "Layout" column in 2.1_Datasets&ObjectTypes.

    value_of_layout_in_type_sheet = {}
    #  type_sheet.values[i + 16][4]--Layout
    if type_sheet.values[i + 16][4] != "" and str(type_sheet.values[i + 16][4]) != "nan":
        try:
            value_of_layout_in_type_sheet = loads('{' + type_sheet.values[i + 16][4] + '}')
        except:
            raise Exception('JSON parse ERROR:\n Can not parse layout data of {} column, {} row in 2.1_Datasets&ObjectTypes to JSON data. Please check.'.format('4', str(i + 16)))
    #----------reading end-------------------------#

    mytemplatetype = {'resource_type': type_sheet.values[i + 16][1].upper(), 'name': type_sheet.values[i + 16][0],
                      'typeattrs': [], 'type_id': i+1}
    #  insert the value of the ObjectTypology from excel. also insert the value of the ObjectType from excel

    # add value of layout in mytemplatetype.
    mytemplatetype['layout'] = value_of_layout_in_type_sheet
    #-------- adding end ------------------#

    # -------------------------------------
    for j in range(len(attr_sheet)):
        #  attr_sheet.values[j][0]--ObjectType of Attributes table
        #  attr_sheet.values[j][1]--AttributeName
        #  attr_sheet.values[j][3]--AttributeUnit
        if type_sheet.values[i + 16][0] == attr_sheet.values[j][0]:
            attr_name = attr_sheet.values[j][1]
            attr_dimension = attr_sheet.values[j][6]
            if (not attr_name in all_attr_dict.keys()) or all_attr_dict.get(attr_name, attr_dimension) is None:
                attr_id = conn.call('add_attribute', {'attr': {'name': attr_sheet.values[j][1], 'dimen': attr_sheet.values[j][6]}})['id']
            else:
                attr_id = all_attr_dict[attr_name.lower()]['id']

            # connect the Template Type (ObjectType) with its Attributes
# Based on the link below, add a unit =AttributeUnit, and a datatype=AttributeDataTypeCV
# http://umwrg.github.io/HydraPlatform/devdocs/HydraServer/index.html?highlight=typeattrs#HydraServer.soap_server.hydra_complexmodels.TypeAttr

            # read value of unit from  "AttributeUnit" column in 2.2_Attributes.
            attr_unit = attr_sheet.values[j][3]
            if not attr_unit:
                attr_unit = ''

            # read value of datatype from  "AttributeDataTypeCV" column in 2.2_Attributes.
            attr_datatype = attr_sheet.values[j][6]
            if not attr_datatype:
                attr_datatype = ''
            elif  attr_datatype =='MultiAttributeSeries':
                attr_datatype='array'
            elif  attr_datatype =='SeasonalNumericValues':
                attr_datatype='array'
            elif attr_datatype =='NumericValues':
                attr_datatype='scalar'
            elif attr_datatype =='TimeSeries':
                attr_datatype='timeseries'
            elif attr_datatype =='DescriptorValues':
                attr_datatype='descriptor'
            elif attr_datatype =='DualValues':
                attr_datatype='descriptor'
            elif attr_datatype == 'AttributeSeries':
                 attr_datatype = 'array'

            mytemplatetype['typeattrs'].append({'type_id': i + 1, 'attr_is_var':True,'attr_id': attr_id,'data_type': attr_datatype})  # type_id for the template table
#,'unit': attr_unit
    # --------------------------------------------


    # Add some object types to the Template Type  (resource type can be NODE, LINK, GROUP, NETWORK)
    template['types'].append(mytemplatetype)

## Load the Template name and types to the Hydra db
tempDB = conn.call('get_templates', {})
flag_exist_template = False
new_template = {}
for template_item in tempDB:
    if template_item['name'] == template['name']:
        flag_exist_template = True
        new_template = conn.call('get_template', {'template_id' : template_item['id']})
        break
else:
    # if not flag_exist_template:
    # print template
    new_template = conn.call('add_template', {'tmpl': template})
    pass


# Build up a dict by attribute names to call them later.

for j in range(len(attr_sheet)):
    if j < 9: continue  # Avoid headers before line 9 in the nodes sheet
    name = attr_sheet.values[j][1]
    dimension = attr_sheet.values[j][6]

## Load the Attributes to the Hydra db
    if all_attr_dict.get(name) is None:
        if attr_sheet.values[j][6] is not None:
            id = conn.call('add_attribute', {'attr': {'name': attr_sheet.values[j][1], 'dimen': attr_sheet.values[j][6]}})[
                'id']
            all_attr_dict[name] = {'id': id, 'dimension': dimension}

# STEP 4: Import WaMDaM Network, Nodes, and links
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# Follow the instructions here
# http://umwrg.github.io/HydraPlatform/tutorials/plug-in/tutorial_json.html

# add_network
network_sheet = wamdam_data['3.1_Networks&Scenarios']
type_id = None
if new_template:
    for templateType in new_template['types']:
        if templateType['resource_type'] == 'NETWORK':
            type_id = templateType['id']
            break

# get the minimum start
# NetworkMinScenarioStartDate= str(network_sheet.values[i][4])
# NetworkMaxScenarioEndDate= str(network_sheet.values[i][5])
#
# NetworkTimeStep = str(network_sheet.values[i][6])
#
# Networklayout={"start": NetworkMinScenarioStartDate, "end": NetworkMaxScenarioEndDate, "timestep": NetworkTimeStep}

Netlayout = "{'settings': {'start': '2000-01-01T00:00:00Z', 'end': '2001-12-31T00:00:00Z', 'timestep': 'day'}}"

network_template = {'name': network_sheet.values[8][0], 'description': network_sheet.values[8][4],
                    'project_id': my_new_project.id, 'types': [{'id': type_id}],'layout':Netlayout}

# add_nodes
nodes_sheet = wamdam_data['3.2_Nodes']

list_node = []

node_lookup = {}

resource_attr_lookup = {}
dict_res_attr = {}
type_id = None
res_id = -1

# /////make dict_res_attr for network//////////

network_res_attr = []
for j in range(len(attr_sheet)):
    if j < 9: continue  # Avoid headers before line 9 in the attribute sheet
    for templateType in new_template['types']:
        if templateType['resource_type'] == 'NETWORK':
            if attr_sheet.values[j][0] == templateType['name']:
                name = attr_sheet.values[j][1]
                dimension = attr_sheet.values[j][6]

            # res_id = (len(list_res_attr) + 1) * -1

                res_attr = {
                    'ref_key': 'NETWORK',
                    'attr_id': all_attr_dict[name]['id'],
                    'id': res_id,
                }
                res_id -= 1
                # resource_attr_lookup[('NETWORK', res_id)] = res_attr
                network_res_attr.append(res_attr)
                dict_res_attr[(network_template['name'], name)] = res_attr
network_template['attributes'] = network_res_attr
# ///////////////////////////////////////////////////////////////////////////////////////

# Iterate over the node instances and assign the parent Object Attributes to each node instance = ResourceAttribute (as in Hydra)
for i in range(len(nodes_sheet)):
    if i < 8: continue  # Avoid headers before line 9 in the nodes sheet

    # Look up the type_id in Hydra for each type
    for templateType in new_template['types']:
        if nodes_sheet.values[i][0] == templateType['name']:
            type_id = templateType['id']
            # print templateType
            break

    if type_id is None:
        raise Exception("Unable to find a type in the template for %s" % nodes_sheet.values[i][0])

    flag = False
    for node_item in list_node:
        if node_item['name'] == nodes_sheet.values[i][1]:
            flag = True
    if flag: continue

    description = str(nodes_sheet.values[i][9])
    if description == "nan":
        description = ""

    name =  nodes_sheet.values[i][1]

    if len(name) > 60:
        log.warn('Node name %s too long. Truncating)', name)
        name = name[0:57] + "..."

    node = {'id': i * -1,
            'name': name,
            'description': description,
            'x': str(nodes_sheet.values[i][7]),
            'y': str(nodes_sheet.values[i][8]),
            'types': [{'id': type_id}]
            }
    node_res_attr = []
    for j in range(len(attr_sheet)):
        if nodes_sheet.values[i][0] == attr_sheet.values[j][0]:
            name = attr_sheet.values[j][1]
            dimension = attr_sheet.values[j][5]

            # res_id = (len(list_res_attr) + 1) * -1

            res_attr = {
                'ref_key': 'NODE',
                'attr_id': all_attr_dict[name]['id'],
                'id': res_id,
            }
            res_id -= 1
            resource_attr_lookup[('NODE', res_id)] = res_attr
            node_res_attr.append(res_attr)
            dict_res_attr[(nodes_sheet.values[i][1], name)] = res_attr

    node['attributes'] = node_res_attr
    list_node.append(node)
    node_lookup[node['name']] = node
network_template['nodes'] = list_node

link_lookup = {}
links_sheet = wamdam_data['3.3_Links']
list_link = []
type_id = None
lst_name = []
for i in range(len(links_sheet)):
    if i < 8: continue  # Avoid headers before line 9 in the links sheet

    for templateType in new_template['types']:
        if links_sheet.values[i][0] == templateType['name']:
            type_id = templateType['id']
            break

    if type_id is None:
        raise Exception("Unable to find a type in the template for %s" % links_sheet.values[i][0])
    description = str(links_sheet.values[i][9])
    if description == "nan":
        description = ""

    name = links_sheet.values[i][1]
    if name in lst_name:
        # print name
        continue
    else:
        lst_name.append(name)

    if len(name) > 60:
        log.warn('Link name %s too long. Truncating)', name)
        name = name[0:57] + "..."

    link = {
        'id': i * -1,
        'name': name,
        'description': description,
        'types': [{'id': type_id}]
    }
    node_a = node_lookup.get(links_sheet.values[i][6])
    if node_a is None:
        raise Exception("Node %s could not be found" % (links_sheet.values[i][6]))
    link['node_1_id'] = node_a['id']
    node_b = node_lookup.get(links_sheet.values[i][7])
    if node_b is None:
        raise Exception("Node %s could not be found" % (links_sheet.values[i][6]))
    link['node_2_id'] = node_b['id']


    # ///// links resource atttribute///////
    link_res_attr = []
    for j in range(len(attr_sheet)):
        if links_sheet.values[i][0] == attr_sheet.values[j][0]:
            name = attr_sheet.values[j][1]
            dimension = attr_sheet.values[j][5]

            # res_id = (len(list_res_attr) + 1) * -1

            res_attr = {
                'ref_key': 'LINK',
                'attr_id': all_attr_dict[name]['id'],
                'id': res_id,
            }
            res_id -= 1
            # resource_attr_lookup[('NODE', res_id)] = res_attr
            link_res_attr.append(res_attr)
            dict_res_attr[(links_sheet.values[i][1], name)] = res_attr
    link['attributes'] = link_res_attr

    list_link.append(link)
    link_lookup[link['name']] = link

network_template['links'] = list_link
network_template['resourcegroups'] = []
# network = conn.call('add_network', {'net':network_template})
## Load the Network, its nodes, and links to the Hydra db

# http://umwrg.github.io/HydraPlatform/tutorials/plug-in/tutorial_json.html#scenarios-and-data

# network = conn.call('add_network', {'net':network_template})


# STEP 5: Import Scenarios and Data Values of Attributes for Nodes and links
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# 5.1 add the scenario
list_scenario = []
for i in range(len(network_sheet)):
    if i < 18: continue  # Avoid headers before line 9 in the 4_NumericValues sheet

    if network_sheet.values[i][0] == None or str(network_sheet.values[i][0]) == "nan":
        # If there is no value in network sheet, stop loop.
        break
    description = str(network_sheet.values[i][8])
    if description == "nan":
        description = ""
    ScenarioName= str(network_sheet.values[i][0])
    ScenarioStartDate= str(network_sheet.values[i][4])
    ScenarioEndDate= str(network_sheet.values[i][5])
    TimeStep = str(network_sheet.values[i][6])
    scenario = {'name': ScenarioName, 'start_time':ScenarioStartDate,'end_time':ScenarioEndDate,'time_step':TimeStep,'description': description, 'resourcescenarios': []}
    list_rs = []

    # Working with Datasets in Hydra which are equivalent to DataValues tables in WaMDaM
    # http://umwrg.github.io/HydraPlatform/tutorials/webservice/datasets.html?highlight=datasets

    # **************************************************
    # 5.2 Numeric Values

    numerical_sheet = wamdam_data['4_NumericValues']

    # Iterate over the rows in the Numeric Values sheet [scalars dataset] and associate the value with resource attribute (node instance and attribute)
    for j in range(8, len(numerical_sheet)):  # //8: reall value row in sheet
        if network_sheet.values[i][0] == numerical_sheet.values[j][2]:
            attr_name = numerical_sheet.values[j][3]
            dimension = all_attr_dict[attr_name]['dimension']
            if (numerical_sheet.values[j][1], numerical_sheet.values[j][3]) in dict_res_attr.keys():
                rs = {'resource_attr_id': dict_res_attr[(numerical_sheet.values[j][1], numerical_sheet.values[j][3])]['id']}
            else:
                raise Exception("Unable to find resource_attr_id for %s" % numerical_sheet.values[j][3])

            dataset = {'type': 'scalar', 'name': attr_name, 'unit': 'ml', 'dimension': dimension,
                       'hidden': 'N', 'value': str(numerical_sheet.values[j][6])}
            # The provided dimension here must match the attribute as defined earlier.

            rs['value'] = dataset
            list_rs.append(rs)
    # associate the values, resources attributes to their scenario
    scenario['resourcescenarios'] = list_rs
    list_scenario.append(scenario)

# network_template['scenarios'] = list_scenario
# #
# network = conn.call('add_network', {'net':network_template})

# ****************************************************
# 5.3 Descriptor Values (4_DescriptorValues )
# Iterate over the rows in the 4_DescriptorValuess sheet and associate the value with its scenario, and resource attribute
Descriptor_sheet = wamdam_data['4_DescriptorValues']

# add the scenario
# list_scenario = []
for i in range(len(network_sheet)):
    if i < 18: continue  # Avoid headers before line 9 in the 4_DescriptorValues sheet

    if network_sheet.values[i][0] == None or str(network_sheet.values[i][0]) == "nan":
        # If there is no value in network sheet, stop loop.
        break
    description = str(network_sheet.values[i][8])
    if description == "nan":
        description = ""
    scenario = {'name': network_sheet.values[i][0], 'description': network_sheet.values[i][8], 'resourcescenarios': []}
    list_rs = []

    # Iterate over the rows in the Numeric Values sheet [scalars dataset] and associate the value with resource attribute (node instance and attribute)
    for j in range(8, len(Descriptor_sheet)):
        if network_sheet.values[i][0] == Descriptor_sheet.values[j][2]:
            attr_name = Descriptor_sheet.values[j][3]
            dimension = all_attr_dict[Descriptor_sheet.values[j][3]]['dimension']

            if (Descriptor_sheet.values[j][1], Descriptor_sheet.values[j][3]) in dict_res_attr.keys():
                rs = {'resource_attr_id': dict_res_attr[(Descriptor_sheet.values[j][1], Descriptor_sheet.values[j][3])]['id']}
            else:
                raise Exception("Unable to find resource_attr_id for %s" % Descriptor_sheet.values[j][3])

            dataset = {'type': 'descriptor', 'name': attr_name, 'unit': 'ml', 'dimension': dimension,
                       'hidden': 'N', 'value': Descriptor_sheet.values[j][6]}
            # The provided dimension here must match the attribute as defined earlier.

            rs['value'] = dataset
            list_rs.append(rs)
    # associate the values, resources attributes to their scenario
    for index in range(len(list_scenario)):
        if list_scenario[index]['name'] == network_sheet.values[i][0]:
            list_scenario[index]['resourcescenarios'].extend(list_rs)
    # scenario['resourcescenarios'] = list_rs
    # list_scenario.append(scenario)

# network_template['scenarios'] = list_scenario
# network = conn.call('add_network', {'net':network_template})
# ******************************************************************************************************************

# 5.4 Descriptor Values (4_DualValues) (does the same like 2.1 but for another sheet)
# Iterate over the rows in the 4_DualValues sheet and associate the value with its scenario, and resource attribute
#  (dual Value here is like DescriptorValue)
Descriptor_sheet = wamdam_data['4_DualValues']

# add the scenario
# list_scenario = []
for i in range(len(network_sheet)):
    if i < 18: continue  # Avoid headers before line 9 in the 4_DualValues sheet

    if network_sheet.values[i][0] == None or str(network_sheet.values[i][0]) == "nan":
        # If there is no value in network sheet, stop loop.
        break

    description = str(network_sheet.values[i][8])
    if description == "nan":
        description = ""
    scenario = {'name': network_sheet.values[i][0], 'description': network_sheet.values[i][8], 'resourcescenarios': []}
    list_rs = []

    # Iterate over the rows in the Numeric Values sheet [scalars dataset] and associate the value with resource attribute
    # (node instance and attribute)
    for j in range(8, len(Descriptor_sheet)):
        if network_sheet.values[i][0] == Descriptor_sheet.values[j][2]:
            attr_name = Descriptor_sheet.values[j][3]
            dimension = all_attr_dict[Descriptor_sheet.values[j][3]]['dimension']
            # look up the unit to each attribute used in the Descriptor_sheet from the 2.2_Attributes sheet (column D)
            # attUnit = Descriptor_sheet.values[j][3]

            if (Descriptor_sheet.values[j][1], Descriptor_sheet.values[j][3]) in dict_res_attr.keys():
                rs = {'resource_attr_id': dict_res_attr[(Descriptor_sheet.values[j][1], Descriptor_sheet.values[j][3])]['id']}
            else:
                raise Exception("Unable to find resource_attr_id for %s" % Descriptor_sheet.values[j][3])

            dataset = {'type': 'descriptor', 'name': attr_name, 'unit': 'ml', 'dimension': dimension,
                       'hidden': 'N', 'value': str(Descriptor_sheet.values[j][6])}
            # The provided dimension here must match the attribute as defined earlier.

            rs['value'] = dataset
            list_rs.append(rs)
    # associate the values, resources attributes to their scenario
    for index in range(len(list_scenario)):
        if list_scenario[index]['name'] == network_sheet.values[i][0]:
            list_scenario[index]['resourcescenarios'].extend(list_rs)
    # scenario['resourcescenarios'] = list_rs
    # list_scenario.append(scenario)
# print list_scenario
# network_template['scenarios'] = list_scenario
# network = conn.call('add_network', {'net':network_template})
# ********************************************************
# 5.5 Time Series
# Iterate over the rows in the 4_TimeSeriesValues sheet and associate the value with its scenario, and resource attribute
# Reference for time series in Hydra: follow this logic
# http://umwrg.github.io/HydraPlatform/devdocs/techdocs/timeseries.html#an-example-in-python

TimeSeriesValues_sheet = wamdam_data['4_TimeSeriesValues']

# add the scenario
# list_scenario = []
for i in range(len(network_sheet)):
    if i < 18: continue  # Avoid headers before line 9 in the 4_TimeSeriesValues sheet
    if network_sheet.values[i][0] == None or str(network_sheet.values[i][0]) == "nan":
        # If there is no value in network sheet, stop loop.
        break

    description = str(network_sheet.values[i][8])
    if description == "nan":
        description = ""
    scenario = {'name': network_sheet.values[i][0], 'description': network_sheet.values[i][8], 'resourcescenarios': []}
    list_rs = []

    # Iterate over the rows in the TimeSeriesValues sheet [scalars dataset] and associate the value with resource attribute
    # (node instance and attribute)
    timeseries_list = {}
    for j in range(8, len(TimeSeriesValues_sheet)):  # //8: reall value row in sheet
        if network_sheet.values[i][0] == TimeSeriesValues_sheet.values[j][2]:
            attr_name = TimeSeriesValues_sheet.values[j][3]
            if (TimeSeriesValues_sheet.values[j][1], attr_name) in timeseries_list.keys():
                timeseries_list[(TimeSeriesValues_sheet.values[j][1], attr_name)].append(
                    (TimeSeriesValues_sheet.values[j][4], TimeSeriesValues_sheet.values[j][5]))
            else:
                values = []
                values.append((TimeSeriesValues_sheet.values[j][4], TimeSeriesValues_sheet.values[j][5]))
                timeseries_list[(TimeSeriesValues_sheet.values[j][1], attr_name)] = values

    for key in timeseries_list.keys():
        timeseries = {"Header": {}, "0": {}}
        for time, value in timeseries_list[key]:
            t = str(time)
            timeseries["0"][t] = value

        # timeseries['ts_values'] = json.dumps(timeseries)

        # attr_name = key
        dimension = all_attr_dict[key[1]]['dimension']

        if key in dict_res_attr.keys():
            rs = {'resource_attr_id': dict_res_attr[key]['id']}
        else:
            raise Exception("Unable to find resource_attr_id for %s" % key)

        # rs = {'resource_attr_id': all_attr_dict[attr_name]['id']}

        dataset = {'type': 'timeseries', 'name': attr_name, 'unit': 'ml', 'dimension': dimension,
                   'hidden': 'N', 'value': json.dumps(timeseries)}
        # The provided dimension here must match the attribute as defined earlier.

        rs['value'] = dataset
        list_rs.append(rs)
    # associate the values, resources attributes to their scenario
    for index in range(len(list_scenario)):
        if list_scenario[index]['name'] == network_sheet.values[i][0]:
            list_scenario[index]['resourcescenarios'].extend(list_rs)
    # scenario['resourcescenarios'] = list_rs
    # list_scenario.append(scenario)
# print list_scenario
# network_template['scenarios'] = list_scenario
# network = conn.call('add_network', {'net':network_template})


# ********************************************************
# 5.6 Arrays
# Iterate over the rows in the MultiColumns Series sheet and associate the value with its scenario, and resource attribute

# Reference for arrays in Hydra (not clear to me yet, an example would help)
#	http://umwrg.github.io/HydraPlatform/tutorials/webservice/datasets.html?highlight=arrays#array-format


# Will add the array values for each attribute
# Here Column D in excel starting row 19 has the attribute name that for the whole array (its just like the attribute for the descriptor)
# Columns G, H,....L, etc starting row 4 in excel have the names of the Array "items" or sub-attributes
# so each value belongs to an Attribute (array name) and a sub-attribute (array item) under an ObjectType and Instance name

multiAttr_sheet = wamdam_data['4_MultiAttributeSeries']
#get attribut field count
con_attributes = {}
for i in range(3, 12):
    if multiAttr_sheet.values[i][5] == None or str(multiAttr_sheet.values[i][5]) == "nan":
        # If there is no value in network sheet, stop loop.
        break
    con_attributes[multiAttr_sheet.values[i][5]] = 0
    for j in range(6, 11):

        if str(multiAttr_sheet.values[i][j]) == 'nan' or multiAttr_sheet.values[i][j] == "":
        # If there is no value in network sheet, stop loop.
            break
        con_attributes[multiAttr_sheet.values[i][5]] = con_attributes[multiAttr_sheet.values[i][5]] + 1


# add the scenario
# list_scenario = []
for i in range(18, len(network_sheet)):
    # if i < 9: continue  # Avoid headers before line 9 in the 4_DescriptorValues sheet

    if network_sheet.values[i][0] == None or str(network_sheet.values[i][0]) == "nan":
        # If there is no value in network sheet, stop loop.
        break

    description = str(network_sheet.values[i][8])
    if description == "nan":
        description = ""
    scenario = {'name': network_sheet.values[i][0], 'description': network_sheet.values[i][8], 'resourcescenarios': []}
    list_rs = []

    # Iterate over the rows in the Numeric Values sheet [scalars dataset] and associate the value with resource attribute (node instance and attribute)
    name = '' #multiarray instance name
    array_value = []
    for j in range(17, len(multiAttr_sheet)):
        if network_sheet.values[i][0] == multiAttr_sheet.values[j][2]:
            if name != multiAttr_sheet.values[j][1]:
                if len(array_value) > 0:
                    dimension = all_attr_dict[multiAttr_sheet.values[j][3]]['dimension']

                    if (multiAttr_sheet.values[j][1], multiAttr_sheet.values[j][3]) in dict_res_attr.keys():
                        rs = {'resource_attr_id': dict_res_attr[(multiAttr_sheet.values[j][1], multiAttr_sheet.values[j][3])]['id']}
                    else:
                        continue
                        raise Exception("Unable to find resource_attr_id for %s" % Descriptor_sheet.values[j][3])
                    dataset = {'type': 'array', 'name': multiAttr_sheet.values[j][3], 'unit': 'ml', 'dimension': dimension, 'hidden': 'N'}

                    dataset['value'] = json.dumps(array_value)
                    # print dataset
                    # dataset['metadata'] = [
                    #     { 'name' : 'ObjectType', 'value' : multiAttr_sheet.values[j-1][0]},
                    #     { 'name' : 'ScenarioName', 'value' : multiAttr_sheet.values[j-1][2]},
                    #     { 'name' : 'SourceName', 'value' : multiAttr_sheet.values[j-1][4]},
                    #     { 'name' : 'MethodName', 'value' : multiAttr_sheet.values[j-1][5]}
                    # ]

                    rs['value'] = dataset
                    list_rs.append(rs)

                name = multiAttr_sheet.values[j][1] # new instance name of multiarray
                array_value = []
                for kk in range(1, con_attributes[multiAttr_sheet.values[j][3]] + 1):
                    templist = []
                    templist.append(multiAttr_sheet.values[j][5 + kk])
                    array_value.append(templist)


            else:
                for kk in range(1, con_attributes[multiAttr_sheet.values[j][3]] + 1):
                    array_value[kk - 1].append(multiAttr_sheet.values[j][5 + kk])
    print array_value
            # The provided dimension here must match the attribute as defined earlier.

            # rs['value'] = dataset
            # list_rs.append(rs)
    # associate the values, resources attributes to their scenario
    for index in range(len(list_scenario)):
        if list_scenario[index]['name'] == network_sheet.values[i][0]:
            list_scenario[index]['resourcescenarios'].extend(list_rs)
    # scenario['resourcescenarios'] = list_rs
    # list_scenario.append(scenario)

network_template['scenarios'] = list_scenario


network = conn.call('add_network', {'net':network_template})

