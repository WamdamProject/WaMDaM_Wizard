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
import json
from pandas.io.json import json_normalize
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


from controller.OpenAgua.Download.NewOA2 import Hydra_OA

# General library for working with JSON objects
import json, copy
# Used for working with files.
import os, sys, datetime

import logging



def UploadToOpenAgua(selectedResourceTypeAcro, selectedMasterNetworkName, selectedScenarioNames, projectName, username_oa, password_oa):
    # selectedResourceTypeAcro='WASH'
    # selectedMasterNetworkName='Lower Bear River Network'
    # selectedScenarioName='base case scenario 2003'
    endpoint = 'https://www.openagua.org/api/v1/hydra/'


    hydra = Hydra_OA(endpoint, username=username_oa,password=password_oa)

    # default_network_name = ''
    # selectedScenarioName = ''

    # pass these as paramters input
    # selectedDataset, selectedMasterNetworkName, selectedScenarioName

    getDataStructure = GetResourceStructure()
    getInstances = GetInstancesBySenario()


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


    # Network = hydra_call(username_oa, password_oa, 'get_network',
    #                     {'network_id': Selected_network_id, 'scenario_id': Selected_scenario_id, 'include_values': 'N',
    #                      'summary': 'Y'})

    # get_all_dimensions=hydra_call(username_oa, password_oa,'get_all_dimensions',{})


    Server_all_dimensions = hydra.call('get_dimensions')

    # Server_all_dimensions_df=pd.DataFrame(Server_all_dimensions)

    # STEP 2: Import the WaMDaM workbook sheets
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



    # type_sheet = wamdam_data['2.1_ResourceTypes&ObjectTypes']
    type_sheet_resourceTypes = getDataStructure.GetResourceType(selectedResourceTypeAcro)
    type_sheet_objectTypes = getDataStructure.GetObjectTypesByResource(selectedResourceTypeAcro)

    # Import the attributes
    # attr_sheet = wamdam_data['2.2_Attributes']
    attr_sheet = getDataStructure.GetAttributesByResource(selectedResourceTypeAcro)
    UnitsTable=GetUnits()
    UnitsTable_df = UnitsTable.GetUnits_dims()





    # STEP 3: Define a project in Hydra. Add the template "dataset name", Object Types and Attributes in Hydra
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    # Use the 'get_projects' call to check for an existing project of this name by listing all available projects.
    # The project concept does not exist in WaMDaM but it is needed in Hydra. We define it here
    projects = hydra.call('get_projects')



    ## Load the new Project name to the Hydra db
    my_new_project = None


    User5char=username_oa[0:4]
    for p in projects:
        if projectName==p['name']:
            my_new_project=p
            projectID=p['id']
            break

    if not my_new_project:
        my_new_project = hydra._call('add_project', {'name': projectName,'description ': 'add pro description'})
        projectID=my_new_project['id']

    # Add the attribute:
    # Attributes in Hydra are independent of ObjectTypes or templates types (they can be shared across object types)

    # Look all the unique attributes in 2.2_Attributes sheet.  Get the AttributeUnit for each attribute.

    # The "Category" in WaMDaM is equivalent to "dimension" in Hydra
    # my_new_attr_list = []
    # my_new_attr = conn.call('add_attribute', {'attr': {'name': ['attr'], 'dimension': ['Volume']}})


    # all_attributes = hydra.call('get_attributes')
    #
    # all_attr_dict = {}
    # for a in all_attributes:
    #     dimension_data = hydra.call('get_dimension',{'dimension_id': a['dimension_id']})
    #     all_attr_dict[(a['name'], dimension_data['name'])] = {'id': a['id'], 'dimension': dimension_data['name']}
    #
    # pd.DataFrame(all_attr_dict.items())

    # -------------------------

    # Create a new template (dataset)
    # This will fail second time around due to a unique naming restriction.
    # You should call 'get_templates' first and update an existing one if one with the same name is already there.

    # 2.1_Datasets&ObjectTypes sheet, look in the Datasets_table
    # DatasetName which is cell A10 in 2.1_Datasets&ObjectTypes sheet

    # concatnate part of the user name into the project name to make globally unique in HydraPlatform
    GlobalTemplate=type_sheet_resourceTypes.values[0][1] #+'_'+User5char


    template = {'name': GlobalTemplate,'description':'add description here', 'templatetypes': []}  # insert the value of the "DatasetName" from excel
    # A template is equivalent to a dataset in wamdam

    # my_templates lists available templates. A template equates to the 'Dataset' in WaMDaM.
    # Go through this worksheet, building a hydra template
    # my_templates = hydra._call('get_template_attributes', {})


    # -----------------------------
    # Go through the excel sheet and pull out the template type definitions...
    # a template type in Hydra is equivalent to an Object Type in WaMDaM
    # resource_type in Hydra is equivalent to an ObjectTypology in WaMDaM
    # typeAttrs (the same as Template Type Attributes) links attributes to their template

    # 2.1_Datasets&ObjectTypes sheet, look in the ObjectTypes_table

    # iterate to get the object types and their attributes
    # start reading from row 16 because value is staring from 16 row.
    Dataset_attr_Name_Dim_list = {}
    Dataset_attr_Name_Dim_unit = {}
    attr_ID_by_Unit_attrName_list = {}

    # use the unites later in the code
    HydraUnits = hydra.call('get_units')



    print 'looping through the object types'
    for i in range(len(type_sheet_objectTypes.values)):

        if type_sheet_objectTypes.values[i][0] == "" or str(type_sheet_objectTypes.values[i][0]) == "None" :
            break
            """"Raise an error message if the Unit Type is missing for any attribute"""

        #  type_sheet.values[i + 16][0]--ObjectType
        #  type_sheet.values[i + 16][1]--ObjectTypology

    #  Based on the link below, add a layout =Icon
    # http://umwrg.github.io/HydraPlatform/devdocs/HydraServer/index.html?highlight=typeattrs#HydraServer.soap_server.hydra_complexmodels.TemplateType

        # layout: {svg: "<svg>...</svg>"}
        # read value of layout from  "Layout" column in 2.1_Datasets&ObjectTypes.

        value_of_layout_in_type_sheet = {}
        #  type_sheet.values[i + 16][4]--Layout
        if type_sheet_objectTypes.values[i][4] != "" and str(type_sheet_objectTypes.values[i][4]) != "None":
            try:
                value_of_layout_in_type_sheet = loads('{' + type_sheet_objectTypes.values[i][4] + '}')
            except:
                raise Exception('JSON parse ERROR:\n Can not parse layout data of {} column, {} row in 2.1_Datasets&ObjectTypes to JSON data. Please check.'.format('4', str(i + 16)))
        #----------reading end-------------------------#

        mytemplatetype = {'resource_type': type_sheet_objectTypes.values[i][1].upper(), 'name': type_sheet_objectTypes.values[i][0],
                          'typeattrs': [], 'type_id': i+1}
        #  insert the value of the ObjectTypology from excel. also insert the value of the ObjectType from excel

        # add value of layout in mytemplatetype.
        mytemplatetype['layout'] = value_of_layout_in_type_sheet
        #-------- adding end ------------------#

        # -------------------------------------

        for j in range(len(attr_sheet.values)):

            if type_sheet_objectTypes.values[i][0] == attr_sheet.values[j][0]:

                # if attr_sheet.values[j][6] == 'AttributeSeries':
                #     continue # dont upload this attribute to the template. Its used in WaMDaM to keep track of the individual attributes
                            # for an array. But Hydra does not have it. Uploading it confused users.

                ObjectType = attr_sheet.values[j][0] #ObjectType
                attr_name = attr_sheet.values[j][1] #AttributeName

                # if attr_name =='Elevation-Curve' or attr_name =='Volume-Curve':
                #     continue


                AttributeUnitCV= attr_sheet.values[j][5]

                try:
                    for server_dim in Server_all_dimensions:
                        units_on_server = server_dim['units']
                        for each_units_on_server in units_on_server:
                            server_unit_name = each_units_on_server['name']

                            if AttributeUnitCV==None:
                                print attr_name + 'for' + ObjectType + 'is required but not provided'
                            elif AttributeUnitCV==server_unit_name:
                                server_dim_name = server_dim['name']

                                server_unit_id = each_units_on_server['id']
                                server_dim_id = each_units_on_server['dimension_id']

                                # if server_unit_id == 243:
                                print ObjectType
                                print server_unit_name
                                print attr_name
                                print server_dim_name
                                print '------------------'
                                break
                                # if server_unit_id==243:
                                #     print server_unit_name
                                #     print attr_name
                                #     break
                except:
                       print 'there is a problem in units. The provided unit in WaMDaM does not exist in the Hydra Server'

                # u'{\'message\': \'Unit 243 (abbreviation=unk) has dimension_id 23(name=dimensionless), but attribute has no dimension\', \'code\': \'0000\'}'

                # try:
                #     # AttributeUnitCV = attr_sheet.values[j][5]
                #     # attr_dimension = UnitsTable_df.loc[UnitsTable_df[0]==AttributeUnitCV].iloc[0,1]
                #     #
                #     # attr_unit = UnitsTable_df.loc[UnitsTable_df[0]==AttributeUnitCV].iloc[0,0]
                #     #
                #     # # look up dimension id from its name
                #     # attr_dimension_id=Server_all_dimensions_df.loc[Server_all_dimensions_df['name'] == attr_dimension]['id'].item()
                #
                #     # print attr_dimension_id
                #     # attr_dimension = UnitsTable_df.loc[UnitsTable_df[2]==AttributeUnit].iloc[0,1]
                #
                # # https://stackoverflow.com/questions/30787901/how-to-get-a-value-from-a-pandas-dataframe-and-not-the-index-and-object-type
                #
                # except:
                #     msg = "There is a problem with looking up units \n. Invalid Key : {} \n Objectype:{}".format(AttributeUnitCV , ObjectType)
                #     raise Exception(msg)
                    # attr_dimension = ''

                # attr_unit=AttributeUnitCV
                # attr_unit=AttributeUnit


                # if not all_attr_dict.get(name,dimension) :
                # if not all_attr_dict.get(attr_name,attr_dimension) :

                # change this
                # We need to add a try statement here. try to add an attribute. if it exists, then we look up the existing attribute id and its dimension

                # try:
                    # https: // github.com / openagua / hydra - base / blob / master / hydra_base / lib / attributes.py  # L120

                    # if not (attr_name, attr_dimension) in all_attr_dict.keys(): #and all_attr_dict[(attr_name, attr_dimension)]['dimension'] == attr_dimension):


                try:
                    # add the attribute. If it exists, then get its id and reuse it

                    resp = hydra._call('add_attribute', {'name': attr_name, 'dimension_id': server_dim_id})
                    if resp and 'id' in resp.keys():
                        server_attr_id = resp['id']

                    else:
                        server_attr = hydra.call('get_attribute_by_name_and_dimension',
                                                 {'name': attr_name, 'dimen': server_dim_name})
                        server_attr_id = server_attr['id']



                except:
                    server_attr = hydra.call('get_attribute_by_name_and_dimension',
                                                 {'name': attr_name, 'dimen': server_dim_name})
                    server_attr_id = server_attr['id']


                # # append thr attribute, its diminsion and id to the all_attr_dict so we can use it later to look up attribute in the resource
                # all_attr_dict

                # Build a list that has attribute id, name, dimension to use it later to look up dimensions for each atrribute below.
                # Dataset_attr_Name_Dim=[ObjectType,attr_dimension,attr_name]
                Dataset_attr_Name_Dim_list[(ObjectType,attr_name)] = server_dim_name

                Dataset_attr_Name_Dim_unit[(ObjectType, attr_name)] = server_unit_name

                # create a dataframe for all these colums together. Now there is an issue in looking up them in these two seperate lists

                attr_ID_by_Unit_attrName_list[(AttributeUnitCV, attr_name)] = server_attr_id

                # server_unit_id
                # server_dim_id
                # server_unit_name
                # server_dim_name

                # connect the Template Type (ObjectType) with its Attributes
                # Based on the link below, add a unit =AttributeUnit, and a datatype=AttributeDataTypeCV
                # http://umwrg.github.io/HydraPlatform/devdocs/HydraServer/index.html?highlight=typeattrs#HydraServer.soap_server.hydra_complexmodels.TypeAttr

                # read value of unit from  "AttributeUnit" column in 2.2_Attributes.
                # attr_unit = attr_sheet.values[j][4]


                AttributeCategory=  attr_sheet.values[j][7]

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

                AttributeScale=int(float(attr_sheet.values[j][10]))

                ModelInputOrOutput=attr_sheet.values[j][8]
                if ModelInputOrOutput=='Output':
                    ModelInputOrOutput='Y' # "Y" (output)
                    Display_data= True
                else:
                    ModelInputOrOutput='N'  #"N" (input) By default its input
                    Display_data= False




                #Get the unit_id from the Hydra server
                # for uni in HydraUnits:
                #     if uni['name']==AttributeUnitCV and attr_dimension_id==uni['dimension_id']:
                #         unit_id=uni['id']
                    # else:
                    #     print "this unit does not exist in Hydra"
                    #     print  AttributeUnitCV

                mytemplatetype['typeattrs'].append({'type_id': i + 1, 'is_var':ModelInputOrOutput,'attr_id': server_attr_id,
                                                    'data_type': attr_datatype,'unit_id': server_unit_id,
                                                    'properties': {'category': AttributeCategory,'scale':AttributeScale,'save':Display_data}})
                    # ,
            # --------------------------------------------
            # ,

            # Add some object types to the Template Type  (resource type can be NODE, LINK, GROUP, NETWORK)
        if 'templatetypes' in template.keys():
            template['templatetypes'].append(mytemplatetype)
        else:
            print('there is no key- templatetypes.')
        # print mytemplatetype

    ## Load the Template name and types to the Hydra db
    tempDB = hydra._call('get_templates')
    flag_exist_template = False

    # here I want a dataframe from the above for loop that has all the columns with values together.
    # Then, later in code, I need to look up these values based on one or two I know.
    # now there is a confusion in values because I'm looking things up differently.
    # temp = copy.deepcopy(Dataset_attr_Name_Dim_list)
    # temp.update(Dataset_attr_Name_Dim_unit)
    # [ObjectType, attr_name, server_dim_name, server_unit_name, server_attr_id]

    for template_item in tempDB:
        if template_item['name'] == template['name']:
            template_item_id=template_item['id']
            print 'The template already exists in OpenAgua'

            flag_exist_template = True
            new_template = hydra.call('get_template', {'template_id' : template_item['id']})
            break

    #print template
    if not flag_exist_template:
        # if not flag_exist_template:
        template['project_id'] = projectID

        # u'{\'message\': \'Unit 6 (abbreviation=ft) has dimension_id 1(name=Length), but attribute has dimension_id 23(name=dimensionless)\', \'code\': \'0000\'}'
        # u'{\'message\': \'Unit 243 (abbreviation=unk) has dimension_id 23(name=dimensionless), but attribute has no dimension\', \'code\': \'0000\'}'


        new_template = hydra._call('add_template', {'name': template['name'],
                                                    'project_id': projectID,
                                                    'templatetypes': template['templatetypes'],
                                                    'description': template['description']})
        print new_template
        print new_template['name']
        template_item_id=new_template['id']
        print 'is uploaded to the server as a new one'



    # STEP 4: Import WaMDaM Network, Nodes, and links
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    network_sheet = getInstances.GetMasterNetworks(selectedResourceTypeAcro)
    NetworkDescription=''
    for i in range(len(network_sheet.values)): # get the number of rows (i.e., networks)
        if selectedMasterNetworkName==network_sheet.values[i][0]:
            NetworkDescription=network_sheet.values[i][4]



    # network_template
    # add_nodes
    # nodes_sheet = wamdam_data['3.2_Nodes']
    for templateType in new_template['templatetypes']:
        if templateType['resource_type'] == 'NETWORK':
            type_id = templateType['id']
            network_template = {'name': selectedMasterNetworkName,
                                'description': NetworkDescription,
                                'project_id': projectID, 'types': [{'id': type_id}],
                                'layout':{'active_template_id':template_item_id}}
            break



    list_node = []

    node_lookup = {}

    resource_attr_lookup = {}
    dict_res_attr = {}
    type_id = None
    res_id = -1

    # /////make dict_res_attr for network//////////

    network_res_attr = []
    for j in range(len(attr_sheet.values)):
        for templateType in new_template['templatetypes']:
            if templateType['resource_type'] == 'NETWORK':
                ObjectType=attr_sheet.values[j][0]
                if ObjectType== templateType['name']:
                    name = attr_sheet.values[j][1]
                    AttributeUnitCV = attr_sheet.values[j][5]


                    attribute_server_id = attr_ID_by_Unit_attrName_list[(AttributeUnitCV, name)]


                    res_attr = {
                        'ref_key': 'NETWORK',
                        'attr_id': attribute_server_id, # this look up is not working
                        'id': res_id,
                        'attr_is_var': 'Y'

                    }
                    res_id -= 1
                    # resource_attr_lookup[('NETWORK', res_id)] = res_attr
                    network_res_attr.append(res_attr)
                    dict_res_attr[(selectedMasterNetworkName, name)] = res_attr
    network_template['attributes'] = network_res_attr
    # ///////////////////////////////////////////////////////////////////////////////////////

    # upload the network from one scenario only
    # WaMDaM allows changing the network for its scenarios but Hydra does not.
    # as a work around, we upload the network from the basline scenario in WaMDaM
    # this solution only works if all the scenario networks are the same in WaMDaM
    # otherwise, the user has to load the data into WaMDaM as many network


    scenario_sheet = getInstances.GetScenarios(selectedResourceTypeAcro, selectedMasterNetworkName)

    print 'looping through scenarios and their networks (nodes and links)'
    ScenarioType_flag = False
    for selectedScenarioName in selectedScenarioNames:

        for s in range(len(scenario_sheet)):
            # only add the selected scenario, one at a time.
            ScenarioParentName = str(scenario_sheet.values[s][8])

            # TO DO: handle a case where two scenarios with "baseline" exist. Maybe raise an exception

            if scenario_sheet.values[s][0] == selectedScenarioName and (ScenarioParentName=='Self' or ScenarioParentName=='self'):
                nodes_sheet = getInstances.GetNodesByScenario(selectedResourceTypeAcro, selectedMasterNetworkName,
                                                              selectedScenarioName)
                # Iterate over the node instances and assign the parent Object Attributes to each node instance = ResourceAttribute (as in Hydra)
                print 'looping through the nodes'
                for n in range(len(nodes_sheet.values)):

                    # Look up the type_id in Hydra for each type
                    for templateType in new_template['templatetypes']:
                        if nodes_sheet.values[n][0] == templateType['name']:
                            type_id = templateType['id']
                            break

                    if type_id is None:
                        raise Exception("Unable to find a type in the template for %s" % nodes_sheet[i][0])

                    flag = False
                    for node_item in list_node:
                        if node_item['name'] == nodes_sheet.values[n][1]:
                            flag = True
                    if flag: continue

                    description = str(nodes_sheet.values[n][9])
                    if description == "None":
                        description = ""

                    fullname = nodes_sheet.values[n][1]
                    nameShort = nodes_sheet.values[n][1]

                    node = {'id': n * -1,
                            'name': nameShort,
                            'description': description,
                            'layout': {'display_name': fullname},
                            'x': str(nodes_sheet.values[n][7]),
                            'y': str(nodes_sheet.values[n][8]),
                            'types': [{'id': type_id}]
                            }
                    node_res_attr = []


                    for tn in range(len(attr_sheet)):
                        if nodes_sheet.values[n][0] == attr_sheet.values[tn][0]:
                            name = attr_sheet.values[tn][1]
                            AttributeUnitCV = attr_sheet.values[tn][5]
                            # server_dim_name = UnitsTable_df.loc[UnitsTable_df[0] == AttributeUnitCV].iloc[0, 1]
                            # dimension = server_dim_name
                            attribute_server_id = attr_ID_by_Unit_attrName_list[(AttributeUnitCV, name)]
                            #
                            # # res_id = (len(list_res_attr) + 1) * -1
                            # if (dimension, name) in Dataset_attr_ID_by_Dim_and_Name_list.keys():
                            #     # look up the attribute id on the server based on the both name,dimension together
                            #     attr_id = Dataset_attr_ID_by_Dim_and_Name_list[(dimension, name)]
                            # else:
                            #     attr_id = hydra._call('add_attribute', {'name': name, 'dimen': dimension})['id']
                            res_attr = {
                                'ref_key': 'NODE',
                                'attr_id': attribute_server_id,
                                'id': res_id,
                                'attr_is_var': 'Y'
                            }

                            res_id -= 1
                            resource_attr_lookup[('NODE', res_id)] = res_attr
                            node_res_attr.append(res_attr)
                            dict_res_attr[(nodes_sheet.values[n][1], name)] = res_attr

                    node['attributes'] = node_res_attr
                    list_node.append(node)
                    node_lookup[node['name']] = node
                network_template['nodes'] = list_node

                link_lookup = {}

                links_sheet = getInstances.GetLinksByScenario(selectedResourceTypeAcro, selectedMasterNetworkName,
                                                              selectedScenarioName)

                list_link = []
                type_id = None
                lst_name = []

                print 'looping through the links'

                for l in range(len(links_sheet)):


                    for templateType in new_template['templatetypes']:
                        if links_sheet.values[l][0] == templateType['name']:
                            type_id = templateType['id']
                            break


                    if type_id is None:
                        print "there is a problem here at line 548"
                        # raise Exception("Unable to find a type in the template for %s" % links_sheet.values[i][0])
                    description = str(links_sheet.values[l][9])

                    if description == "None":
                        description = ""

                    name = links_sheet.values[l][1]
                    fullname = links_sheet.values[l][1]

                    if name in lst_name:
                        # print name
                        continue
                    else:
                        lst_name.append(name)

                    link = {
                        'id': l * -1,
                        'name': name,
                        'description': description,
                        'layout': {'display_name': fullname},
                        'types': [{'id': type_id}]
                    }
                    node_a = node_lookup.get(links_sheet.values[l][6])
                    if node_a is None:
                        print "there is a problem here at line 572"
                        # raise Exception("Node %s could not be found" % (links_sheet.values[i][6]))
                    link['node_1_id'] = node_a['id']

                    node_b = node_lookup.get(links_sheet.values[l][7])

                    if node_b is None:
                        print "there is a problem here at line 577"
                        # raise Exception("Node %s could not be found" % (links_sheet.values[i][7]))
                    link['node_2_id'] = node_b['id']

                    # ///// links resource attribute///////

                    link_res_attr = []
                    try:

                        for tl in range(len(attr_sheet)): # issue in l=11
                            if links_sheet.values[l][0] == attr_sheet.values[tl][0]:
                                name = attr_sheet.values[tl][1]
                                AttributeUnitCV = attr_sheet.values[tl][5]


                                attribute_server_id = attr_ID_by_Unit_attrName_list[(AttributeUnitCV, name)]

                                res_attr = {
                                    'ref_key': 'LINK',
                                    'attr_id': attribute_server_id,
                                    'id': res_id,
                                    'attr_is_var': 'Y'

                                }
                                res_id -= 1
                                # resource_attr_lookup[('NODE', res_id)] = res_attr
                                link_res_attr.append(res_attr)
                                dict_res_attr[(links_sheet.values[l][1], name)] = res_attr
                        link['attributes'] = link_res_attr

                        list_link.append(link)
                        link_lookup[link['name']] = link
                    except:
                        print ' there is an issue in creating links resource attribute part'

                network_template['links'] = list_link
                network_template['resourcegroups'] = []
                ScenarioType_flag=True
                break
    if not ScenarioType_flag:
        print "there is a problem here at line 613"
        # raise Exception("""None of the selected Scenarios types has a "Self" ScenarioParentName
        #                  \n
        #                   Make sure that one of the selected scenarios has is a parent scenario
        #                  """)
            # else:
            #     raise Exception("""None of the selected Scenarios types has a "Baseline" Scenario type \n
            #      Make sure that one of the selected scenarios has is a baseline scenario
            #     """)




    print 'go through the scenarios data'
    from Upload_ScenarioData import PrepareScenarioData

    list_scenario = PrepareScenarioData(selectedResourceTypeAcro, selectedMasterNetworkName, selectedScenarioNames, scenario_sheet,dict_res_attr,
                            Dataset_attr_Name_Dim_list, Dataset_attr_Name_Dim_unit,HydraUnits)

    # join all the scenarios into one indexed list [0][xxxxxxxxxxxx], [1][yyyyyyyyyyy], etc based on the # of scenarios jjj
    #
    network_template['scenarios']=list_scenario


    network = hydra._call('add_network', network_template)

    print network

    print 'Successfully uploaded a WaMDaM data to OpenAgua'

    # active_template_id

    # append the child scenarios to their parent


    # first call just uploaded network and scenarios and get their IDs, names, and description


    # commeted out all this block below
    GetNetworks_metadata = hydra.call('get_networks', {'project_id': projectID, 'include_data': 'N'})
    GetNetworks_metadata_df = json_normalize(GetNetworks_metadata)


    for network_row in GetNetworks_metadata_df.iterrows():
        if network_row[1]['name'] == selectedMasterNetworkName:
            network_id = network_row[1]['id']
            break


    # Get all the scenarios inside the uploaded network
    Get_scenarios_metadata = hydra.call('get_scenarios', {'network_id': network_id})

    Get_scenarios_metadata_df = json_normalize(Get_scenarios_metadata)

    # Use the scenario name to look up its ID
    print 'ready to relate scenarios'


    if len(scenario_sheet) > 1:  # if only once scenario is selected, then dont worry about the parent/child stuff

        for i in range(len(scenario_sheet)):
            for row in Get_scenarios_metadata_df.iterrows():
                ScenarioName_sheet = scenario_sheet.values[i][0]
                ScenarioParentName = scenario_sheet.values[i][8]
                if ScenarioParentName == 'self' or ScenarioParentName == 'Self':
                    if ScenarioName_sheet== row[1]['name']: # matching the spreadsheet with the online uploaded scenario
                        ScenarioParentID=row[1]['id']


            for row in Get_scenarios_metadata_df.iterrows():
                ScenarioName_sheet = scenario_sheet.values[i][0]
                ScenarioParentName = scenario_sheet.values[i][8]
                if not ScenarioParentName == 'self' and not ScenarioParentName == 'Self':
                    if ScenarioName_sheet == row[1]['name']:  # matching the spreadsheet with the online uploaded scenario
                        ChildScenarioID = row[1]['id']
                        ScenarioName_sheet = row[1]['name']
                        # Scenario_description = row[1]['description']

                        # ScenarioType = scenario_sheet.values[i][9].lower()

                        # if ScenarioType == '':
                        #     ScenarioType = 'scenario'

                        scenario = hydra._call('get_scenario', ChildScenarioID)

                        scenario['parent_id'] = ScenarioParentID
                        # scenario['layout': {'class': ScenarioType }] = ScenarioType

                        result = hydra._call('update_scenario', scenario)


                        # print result

                        print 'updated scenario '+ ScenarioName_sheet

    print 'done'
