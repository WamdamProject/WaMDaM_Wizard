# coding: utf-8

# ...layout: {svg: "<svg>...</svg>"}

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


# url = "http://server.basinit.hydra.org.uk/"
# conn = JsonConnection(url)
# login_response = conn.login('amabdallah@aggiemail.usu.edu', 'Hydra2017')



get_all_dimensions=conn.call('get_all_dimensions', ({}))

# STEP 2: Import the WaMDaM workbook sheets
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



# Load the excel file into pandas
# wamdam_data = pd.read_excel('./Qatar3.xlsm', sheetname=None)
# wamdam_data = pd.read_excel('./WASH_June_2018_Hydra.xlsm', sheetname=None)


wamdam_data = pd.read_excel('./PRB_14_WEAP.xlsm', sheetname=None)
# wamdam_data = pd.read_excel('./WEAP_July_2018.xlsm', sheetname=None)

#WEAP_July_2018_Network

# This returns an object, which is a dictionary of pandas 'dataframe'.
# The keys are sheet names and the dataframes are the sheets themselves.
wamdam_data.keys()

# Define the WaMDaM sheets to import
# Import the Datasets and Object Types
type_sheet = wamdam_data['2.1_ResourceTypes&ObjectTypes']

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
    all_attr_dict[(a.name, a.dimen)] = {'id': a.id, 'dimension': a.dimen}


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
Dataset_attr_Name_Dim_list = {}
for i in range(len(type_sheet)):
    if type_sheet.values[i + 16][0] == "" or str(type_sheet.values[i + 16][0]) == "nan" :
        break
    #  type_sheet.values[i + 16][0]--ObjectType
    #  type_sheet.values[i + 16][1]--ObjectTypology

#  Based on the link below, add a layout =Icon
# http://umwrg.github.io/HydraPlatform/devdocs/HydraServer/index.html?highlight=typeattrs#HydraServer.soap_server.hydra_complexmodels.TemplateType

    # layout: {svg: "<svg>...</svg>"}
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
            ObjectType=attr_sheet.values[j][0] #ObjectType
            attr_name = attr_sheet.values[j][1] #AttributeName
            attr_dimension = attr_sheet.values[j][10].strip()




            # if not all_attr_dict.get(name,dimension) :
            # if not all_attr_dict.get(attr_name,attr_dimension) :
            if not (attr_name, attr_dimension) in all_attr_dict.keys(): #and all_attr_dict[(attr_name, attr_dimension)]['dimension'] == attr_dimension):
                attr_id = conn.call('add_attribute', {'attr': {'name': attr_name, 'dimen': attr_dimension}})['id']

            else:
                tem = all_attr_dict[attr_name, attr_dimension]
                # x=all_attr_dict.keys()
                attr_id = tem['id']

            # Build a list that has attribute id, name, dimension to use it later to look up dimensions for each atrribute below.
            # Dataset_attr_Name_Dim=[ObjectType,attr_dimension,attr_name]
            Dataset_attr_Name_Dim_list[(ObjectType,attr_name)] = attr_dimension



            #
            # Temp_all_attr_dict.append()

            # connect the Template Type (ObjectType) with its Attributes
# Based on the link below, add a unit =AttributeUnit, and a datatype=AttributeDataTypeCV
# http://umwrg.github.io/HydraPlatform/devdocs/HydraServer/index.html?highlight=typeattrs#HydraServer.soap_server.hydra_complexmodels.TypeAttr

            # read value of unit from  "AttributeUnit" column in 2.2_Attributes.
            attr_unit = attr_sheet.values[j][4]
            if not attr_unit:
                attr_unit = ''

            # read value of datatype from  "AttributeDataTypeCV" column in 2.2_Attributes.
            attr_datatype = attr_sheet.values[j][6]
            if not attr_datatype:
                attr_datatype = ''
            elif  attr_datatype =='MultiAttributeSeries':
                attr_datatype='array'

            elif  attr_datatype =='SeasonalNumericValues':
                attr_datatype='periodic timeseries'

            elif attr_datatype =='NumericValues':
                attr_datatype='scalar'

            elif attr_datatype =='TimeSeries':
                attr_datatype='timeseries'

            elif attr_datatype =='FreeText':
                attr_datatype='descriptor'

            elif attr_datatype == 'CategoricalValues':
                attr_datatype = 'descriptor'
            #
            elif attr_datatype == 'AttributeSeries':
                 attr_datatype = 'array'

            mytemplatetype['typeattrs'].append({'type_id': i + 1, 'attr_is_var':True,'attr_id': attr_id,'data_type': attr_datatype})  # ,'unit': attr_unit,'unit': attr_unit type_id for the template table
# ,
    # --------------------------------------------
    # ,

    # Add some object types to the Template Type  (resource type can be NODE, LINK, GROUP, NETWORK)
    template['types'].append(mytemplatetype)
    # print mytemplatetype
# print Dataset_attr_Name_Dim_list

## Load the Template name and types to the Hydra db
tempDB = conn.call('get_templates', {})
flag_exist_template = False
for template_item in tempDB:
    if template_item['name'] == template['name']:
        flag_exist_template = True
        new_template = conn.call('get_template', {'template_id' : template_item['id']})
        break

#print template
if not flag_exist_template:
    # if not flag_exist_template:
    # save template to csv to check if it has duplicates

        new_template = conn.call('add_template', {'tmpl': template})
        # print new_template
print 'new_template is uploaded to the server'

# # Build up a dict by attribute names to call them later.
# for j in range(len(attr_sheet)):
#     if j < 9: continue  # Avoid headers before line 9 in the nodes sheet
#     name = attr_sheet.values[j][1]
#     dimension = attr_sheet.values[j][5].strip()

# ## Load the Attributes to the Hydra db. Check if they exist in the server. if they dont, then add them
#     if not all_attr_dict.get(name,dimension) :
#         id = conn.call('add_attribute', {'attr': {'name': attr_sheet.values[j][1], 'dimen': attr_sheet.values[j][5]}})[
#             'id']
#         all_attr_dict[name] = {'id': id, 'dimension': dimension}
#     else:
#         pass
# print 'new attributes are uploaded to the server'


# STEP 4: Import WaMDaM Network, Nodes, and links
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# Follow the instructions here
# http://umwrg.github.io/HydraPlatform/tutorials/plug-in/tutorial_json.html

# add_network
network_sheet = wamdam_data['3.1_Networks&Scenarios']

for templateType in new_template['types']:
    if templateType['resource_type'] == 'NETWORK':
        type_id = templateType['id']
        break

# ScenarioStartDate
# ScenarioEndDate
ScenarioStartDate= str(network_sheet.values[18][4])
ScenarioEndDate= str(network_sheet.values[18][5])
TimeStep = str(network_sheet.values[18][7]) #TimeStepUnitCV


settings_str={'template':template['name'],'start': ScenarioStartDate, 'end': ScenarioEndDate, 'timestep': TimeStep}

Netlayout = {'settings': settings_str}



network_template = {'template':template['name'],'name': network_sheet.values[8][0], 'description': network_sheet.values[8][4],
                    'project_id': my_new_project.id, 'types': [{'id': type_id}],'layout':Netlayout}
# network_template
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
                dimension = attr_sheet.values[j][10]

            # res_id = (len(list_res_attr) + 1) * -1

                res_attr = {
                    'ref_key': 'NETWORK',
                    'attr_id': all_attr_dict[(name,dimension)]['id'],
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

    fullname =  nodes_sheet.values[i][1]
    nameShort =  nodes_sheet.values[i][1]

    # if len(nameShort) > 60:
    #     log.warn('Node name %s too long. Truncating)', nameShort)
    #     nameShort = nameShort[0:57] + "..."

    node = {'id': i * -1,
            'name': nameShort,
            'description': description,
            'layout':{'display_name':fullname},
            'x': str(nodes_sheet.values[i][7]),
            'y': str(nodes_sheet.values[i][8]),
            'types': [{'id': type_id}]
            }
    node_res_attr = []
    for j in range(len(attr_sheet)):
        if nodes_sheet.values[i][0] == attr_sheet.values[j][0]:
            name = attr_sheet.values[j][1]
            dimension = attr_sheet.values[j][10]

            # res_id = (len(list_res_attr) + 1) * -1
            if (name, dimension) in all_attr_dict.keys():
                # look up the attribute id on the server based on the both name,dimension together
                attr_id = all_attr_dict[(name,dimension)]['id']
            else:
                attr_id = conn.call('add_attribute', {'attr': {'name': name, 'dimen': dimension}})['id']
            res_attr = {
                'ref_key': 'NODE',
                'attr_id': attr_id,
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
    fullname = links_sheet.values[i][1]

    if name in lst_name:
        # print name
        continue
    else:
        lst_name.append(name)

    # if len(name) > 60:
    #     log.warn('Link name %s too long. Truncating)', name)
    #     name = name[0:57] + "..."


    link = {
        'id': i * -1,
        'name': name,
        'description': description,
        'layout': {'display_name': fullname},
        'types': [{'id': type_id}]
    }
    node_a = node_lookup.get(links_sheet.values[i][6])
    if node_a is None:
        raise Exception("Node %s could not be found" % (links_sheet.values[i][6]))
    link['node_1_id'] = node_a['id']
    node_b = node_lookup.get(links_sheet.values[i][7])
    if node_b is None:
        raise Exception("Node %s could not be found" % (links_sheet.values[i][7]))
    link['node_2_id'] = node_b['id']


    # ///// links resource atttribute///////
    link_res_attr = []
    for j in range(len(attr_sheet)):
        if links_sheet.values[i][0] == attr_sheet.values[j][0]:
            name = attr_sheet.values[j][1]
            dimension = attr_sheet.values[j][10]

            # res_id = (len(list_res_attr) + 1) * -1

            res_attr = {
                'ref_key': 'LINK',
                'attr_id': all_attr_dict[(name,dimension)]['id'],
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

    startdate=network_sheet.values[i][4]
    try:
        ScenarioStartDate = datetime.datetime.strptime(str(startdate), "%Y/%m/%d").isoformat()
    except:
        ScenarioStartDate = startdate.isoformat()


    enddate=network_sheet.values[i][5]
    try:
        ScenarioStartDate = datetime.datetime.strptime(str(enddate), "%Y/%m/%d").isoformat()
    except:
        ScenarioStartDate = enddate.isoformat()


    TimeStep = str(network_sheet.values[i][7])
    #

    scenario = {'name': ScenarioName, 'start_time':ScenarioStartDate,'end_time':ScenarioEndDate,'time_step':TimeStep,'description': description, 'resourcescenarios': []}
    list_rs_num = []

    # Working with Datasets in Hydra which are equivalent to DataValues tables in WaMDaM
    # http://umwrg.github.io/HydraPlatform/tutorials/webservice/datasets.html?highlight=datasets

    # **************************************************
    # 5.2 Numeric Values

    numerical_sheet = wamdam_data['4_NumericValues']

    # Iterate over the rows in the Numeric Values sheet [scalars dataset] and associate the value with resource attribute (node instance and attribute)
    for j in range(8, len(numerical_sheet)):  # //8: reall value row in sheet
        if network_sheet.values[i][0] == numerical_sheet.values[j][2]:
            attr_name = numerical_sheet.values[j][3]
            ObjectType = numerical_sheet.values[j][0]

            # Dataset_attr_Name_Dim=[ObjectType,attr_dimension,attr_name]

            # look up the dimension using Dataset_attr_Name_Dim based on (attr_name, ObjectType)
            dimension =Dataset_attr_Name_Dim_list[ObjectType, attr_name]

            if (numerical_sheet.values[j][1], numerical_sheet.values[j][3]) in dict_res_attr.keys():
                rs_num = {'resource_attr_id': dict_res_attr[(numerical_sheet.values[j][1], numerical_sheet.values[j][3])]['id']}
            else:
                raise Exception("Unable to find resource_attr_id for %s" % numerical_sheet.values[j][3])

            dataset = {'type': 'scalar', 'name': attr_name, 'unit': '-', 'dimension': dimension,
                       'hidden': 'N', 'value': str(numerical_sheet.values[j][6])}
            # The provided dimension here must match the attribute as defined earlier.

            rs_num['value'] = dataset
            list_rs_num.append(rs_num)
    # associate the values, resources attributes to their scenario
    scenario['resourcescenarios'] = list_rs_num
    list_scenario.append(scenario)

# network_template['scenarios'] = list_scenario
# #
# network = conn.call('add_network', {'net':network_template})

# ****************************************************
# 5.3 4_FreeText Values (4_FreeText )
# Iterate over the rows in the 4_FreeText sheet and associate the value with its scenario, and resource attribute
    Descriptor_sheet = wamdam_data['4_FreeText']

    list_rs_desc=[]
    # Iterate over the rows in the Numeric Values sheet [scalars dataset] and associate the value with resource attribute (node instance and attribute)
    for j in range(8, len(Descriptor_sheet)):
        if network_sheet.values[i][0] == Descriptor_sheet.values[j][2]:
            ObjectType = Descriptor_sheet.values[j][0] #ObjectType
            attr_name = Descriptor_sheet.values[j][3] #AttributeName
            dimension =Dataset_attr_Name_Dim_list[ObjectType,attr_name]


            if (Descriptor_sheet.values[j][1], Descriptor_sheet.values[j][3]) in dict_res_attr.keys():
                rs_desc = {'resource_attr_id': dict_res_attr[(Descriptor_sheet.values[j][1], Descriptor_sheet.values[j][3])]['id']}
            else:
                raise Exception("Unable to find resource_attr_id for %s" % Descriptor_sheet.values[j][3])

            dataset = {'type': 'descriptor', 'name': attr_name, 'unit': '-', 'dimension': dimension,
                       'hidden': 'N', 'value': str(Descriptor_sheet.values[j][6])}
            # print dataset
            # The provided dimension here must match the attribute as defined earlier.

            rs_desc['value'] = dataset
            list_rs_desc.append(rs_desc)
    # associate the values, resources attributes to their scenario
    for index in range(len(list_scenario)):
        if list_scenario[index]['name'] == network_sheet.values[i][0]:
            list_scenario[index]['resourcescenarios'].extend(list_rs_desc)
    # scenario['resourcescenarios'] = list_rs
    # list_scenario.append(scenario)

# network_template['scenarios'] = list_scenario
# network = conn.call('add_network', {'net':network_template})
# ******************************************************************************************************************

# 5.7 Seasonal

# http://umwrg.github.io/HydraPlatform/devdocs/techdocs/timeseries.html?highlight=seasonal#normal-time-series-and-seasonal-time-series

    SeasonalNumericValues_sheet = wamdam_data['4_SeasonalNumericValues']

            # add new script here (see time series above)

    seasonal_list = {}
    list_rs_seas=[]
    for j in range(8, len(SeasonalNumericValues_sheet)):  # //8: reall value row in sheet
        if network_sheet.values[i][0] == SeasonalNumericValues_sheet.values[j][2]:
            attr_name = SeasonalNumericValues_sheet.values[j][3]
            if (SeasonalNumericValues_sheet.values[j][1], attr_name) in seasonal_list.keys():
                seasonal_list[(SeasonalNumericValues_sheet.values[j][1], attr_name)].append(
                    (SeasonalNumericValues_sheet.values[j][9], SeasonalNumericValues_sheet.values[j][8]))
            else:
                values = []
                values.append((SeasonalNumericValues_sheet.values[j][9], SeasonalNumericValues_sheet.values[j][8]))
                seasonal_list[(SeasonalNumericValues_sheet.values[j][1], attr_name)] = values
    # df = pd.DataFrame()
    for key in seasonal_list.keys():
        seasonals = {"Header": {}, "0": {}}
        for time, value in seasonal_list[key]:
            try:
                t = datetime.datetime.strptime(str(time), "%Y/%m/%d").isoformat()
            except:
                t = time.isoformat()
            seasonals["0"][t] = value

        # dimension = all_attr_dict[key[1]]['dimension']
        attr_name=SeasonalNumericValues_sheet.values[j][3]
        ObjectType = SeasonalNumericValues_sheet.values[j][0]

        dimension = Dataset_attr_Name_Dim_list[ObjectType, attr_name]

        if key in dict_res_attr.keys():
            rs_seas = {'resource_attr_id': dict_res_attr[key]['id']}
        else:
            raise Exception("Unable to find resource_attr_id for %s" % key)

        # rs = {'resource_attr_id': all_attr_dict[attr_name]['id']}

        dataset = {'type': 'timeseries', 'name': attr_name, 'unit': 'metre [m', 'dimension': dimension,
                   'hidden': 'N', 'value': json.dumps(seasonals)}
        # The provided dimension here must match the attribute as defined earlier.

        # tsdata.ts_time = PluginLib.date_to_string(time, seasonal=True)

        rs_seas['value'] = dataset
        list_rs_seas.append(rs_seas)
    # associate the values, resources attributes to their scenario
    for index in range(len(list_scenario)):
        if list_scenario[index]['name'] == network_sheet.values[i][0]:
            list_scenario[index]['resourcescenarios'].extend(list_rs_seas)
    # scenario['resourcescenarios'] = list_rs
    # list_scenario.append(scenario)


# 5.5 Time Series
# Iterate over the rows in the 4_TimeSeriesValues sheet and associate the value with its scenario, and resource attribute
# Reference for time series in Hydra: follow this logic
# http://umwrg.github.io/HydraPlatform/devdocs/techdocs/timeseries.html#an-example-in-python

    TimeSeriesValues_sheet = wamdam_data['4_TimeSeriesValues']

# add the scenario
# list_scenario = []
# for i in range(len(network_sheet)):
#     if i < 18: continue  # Avoid headers before line 9 in the 4_TimeSeriesValues sheet
#     if network_sheet.values[i][0] == None or str(network_sheet.values[i][0]) == "nan":
#         # If there is no value in network sheet, stop loop.
#         break
#
#     description = str(network_sheet.values[i][8])
#     if description == "nan":
#         description = ""
#     scenario = {'name': network_sheet.values[i][0], 'description': network_sheet.values[i][8], 'resourcescenarios': []}
#     list_rs = []

    # Iterate over the rows in the TimeSeriesValues sheet [dataset] and associate the value with resource attribute
    # (node instance and attribute)
    timeseries_list = {}
    list_rs_ts=[]
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
            try:
                if isinstance(time, datetime.datetime):
                    ts = time.isoformat()
                else:
                    ts = datetime.datetime.strptime(str(time), "%d/%m/%y").isoformat()
                timeseries["0"][ts] = value
            except:
                ts= datetime.datetime.strptime(str(time), "%m/%d/%Y").isoformat()

                timeseries["0"][ts] = value

        # timeseries['ts_values'] = json.dumps(timeseries)

        ObjectType = TimeSeriesValues_sheet.values[j][0]
        attr_name=TimeSeriesValues_sheet.values[j][3]
        dimension = Dataset_attr_Name_Dim_list[ObjectType,attr_name ]

        if key in dict_res_attr.keys():
            rs_ts = {'resource_attr_id': dict_res_attr[key]['id']}
        else:
            raise Exception("Unable to find resource_attr_id for %s" % key)

        # rs = {'resource_attr_id': all_attr_dict[attr_name]['id']}

        dataset = {'type': 'timeseries', 'name': attr_name, 'unit': 'Cubic metre [m3]', 'dimension': dimension,
                   'hidden': 'N', 'value': json.dumps(timeseries)}
        # The provided dimension here must match the attribute as defined earlier.

        rs_ts['value'] = dataset
        list_rs_ts.append(rs_ts)
    # associate the values, resources attributes to their scenario
    for index in range(len(list_scenario)):
        if list_scenario[index]['name'] == network_sheet.values[i][0]:
            list_scenario[index]['resourcescenarios'].extend(list_rs_ts)
    # scenario['resourcescenarios'] = list_rs
    # list_scenario.append(scenario)


# ********************************************************
# 5.6 Arrays
# Iterate over the rows in the MultiColumns Series sheet and associate the value with its scenario, and resource attribute

# Reference for arrays in Hydra (not clear to me yet, an example would help)
#	http://umwrg.github.io/HydraPlatform/tutorials/webservice/datasets.html?highlight=arrays#array-format


# Will add the array values for each attribute
# Will add the array values for each attribute
# Here Column D in excel starting row 19 has the attribute name that for the whole array (its just like the attribute for the descriptor)
# Columns G, H,....L, etc starting row 4 in excel have the names of the Array "items" or sub-attributes
# so each value belongs to an Attribute (array name) and a sub-attribute (array item) under an ObjectType and Instance name


multiAttr_sheet = wamdam_data['4_MultiAttributeSeries']
#get attribut field count
con_attributes = {}
# upper table
for i in range(3, 12):
    if multiAttr_sheet.values[i][5] == None or str(multiAttr_sheet.values[i][5]) == "nan":
        # If there is no value in network sheet, stop loop.
        break
    con_attributes[multiAttr_sheet.values[i][5]] = 0
    # upper table attributes
    for j in range(6, 11):
        if str(multiAttr_sheet.values[i][j]) == 'nan' or multiAttr_sheet.values[i][j] == "":
        # If there is no values sheet, stop loop.
            break
        con_attributes[multiAttr_sheet.values[i][5]] = con_attributes[multiAttr_sheet.values[i][5]] + 1

#
# add the scenario
for i in range(18, len(network_sheet)):
    # if i < 9: continue  # Avoid headers before line 9 in the 4_DescriptorValues sheet

    # if network_sheet.values[i][0] == None or str(network_sheet.values[i][0]) == "nan":
    #     # If there is no value in network sheet, stop loop.
    #     break
    #
    # description = str(network_sheet.values[i][8])
    # if description == "nan":
    #     description = ""
    # scenario = {'name': network_sheet.values[i][0], 'description': network_sheet.values[i][8], 'resourcescenarios': []}

    # Iterate over the rows in the multiAttr_sheet Values sheet  and associate the value with resource attribute
    # (node instance and attribute)
    name = '' #multiarray instance name
    list_rs_multi=[]
    array_value = []
    for j in range(17, len(multiAttr_sheet)):
        if network_sheet.values[i][0] == multiAttr_sheet.values[j][2]:
            if name != multiAttr_sheet.values[j][1]:
                if len(array_value) > 0 :
                    # Use the attribuite id to look up its dimension
                    ObjectType = multiAttr_sheet.values[j][0]
                    attr_name=multiAttr_sheet.values[j][3]
                    dimension = Dataset_attr_Name_Dim_list[ObjectType,attr_name]
                    # unitname=all_attr_dict[multiAttr_sheet.values[j][3]]['dimension']
                    if (multiAttr_sheet.values[j][1], multiAttr_sheet.values[j][3]) in dict_res_attr.keys():
                        rs_multi = {'resource_attr_id': dict_res_attr[(name, multiAttr_sheet.values[j-1][3])]['id']}
                    else:
                        raise Exception("Unable to find resource_attr_id for %s" % multiAttr_sheet.values[j][3])
                    dataset = {'type': 'array', 'name': multiAttr_sheet.values[j][3], 'unit': '', 'dimension': dimension, 'hidden': 'N'}

                    dataset['value'] = json.dumps(array_value)
                    print dataset
                    # dataset['metadata'] = [
                    #     { 'name' : 'ObjectType', 'value' : multiAttr_sheet.values[j-1][0]},
                    #     { 'name' : 'ScenarioName', 'value' : multiAttr_sheet.values[j-1][2]},
                    #     { 'name' : 'SourceName', 'value' : multiAttr_sheet.values[j-1][4]},
                    #     { 'name' : 'MethodName', 'value' : multiAttr_sheet.values[j-1][5]}
                    # ]
                    rs_multi['value'] = dataset
                    list_rs_multi.append(rs_multi)
                    array_value = []

                name = multiAttr_sheet.values[j][1] # new instance name of multiarray
                # array_value = []
                for kk in range(1, con_attributes[multiAttr_sheet.values[j][3]] + 1):
                    templist = []
                    templist.append(multiAttr_sheet.values[j][5 + kk])
                    array_value.append(templist)

            else:
                for kk in range(1, con_attributes[multiAttr_sheet.values[j][3]] + 1):
                    array_value[kk - 1].append(multiAttr_sheet.values[j][5 + kk])

    if len(array_value) > 0:
        if (multiAttr_sheet.values[j][1], multiAttr_sheet.values[j][3]) in dict_res_attr.keys():

            attr_name = multiAttr_sheet.values[j][3]
            ObjectType = multiAttr_sheet.values[j][0]
            dimension = Dataset_attr_Name_Dim_list[ObjectType,attr_name]

            # unitname = all_attr_dict[multiAttr_sheet.values[j][3]]['unit']

            rs_multi = {'resource_attr_id': dict_res_attr[(multiAttr_sheet.values[j][1], multiAttr_sheet.values[j][3])]['id']}

            dataset = {'type': 'array', 'name': multiAttr_sheet.values[j][3], 'unit': '', 'dimension': dimension,
                               'hidden': 'N', 'value': json.dumps(array_value)}
            rs_multi['value'] = dataset
            list_rs_multi.append(rs_multi)
            print list_rs_multi
        # print rs
        # print array_value
        # The provided dimension here must match the attribute as defined earlier.


                    # rs['value'] = dataset
                    # list_rs.append(rs)
    # associate the values, resources attributes to their scenario
    for index in range(len(list_scenario)):
        if list_scenario[index]['name'] == network_sheet.values[i][0]:
            list_scenario[index]['resourcescenarios'].extend(list_rs_multi)

        # scenario['resourcescenarios'] = list_rs
        # list_scenario.append(scenario)
# print list_rs_multi

network_template['scenarios'] = list_scenario

#print list_scenario

# print network_template
# print network_template
network = conn.call('add_network', {'net':network_template})


