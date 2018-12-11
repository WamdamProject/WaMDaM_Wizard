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





def UploadToOpenAgua(selectedResourceTypeAcro, selectedMasterNetworkName, selectedScenarioNames, projectName):
    # selectedResourceTypeAcro='WASH'
    # selectedMasterNetworkName='Lower Bear River Network'
    # selectedScenarioName='base case scenario 2003'



    # default_network_name = ''
    # selectedScenarioName = ''

    # pass these as paramters input
    # selectedDataset, selectedMasterNetworkName, selectedScenarioName

    getDataStructure = GetResourceStructure()
    getInstances = GetInstancesBySenario()
    getValuesAll = GetAllValuesByScenario()

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

    get_all_dimensions=conn.call('get_all_dimensions', ({}))

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
    projects = conn.call('get_projects', {})

    ## Load the new Project name to the Hydra db
    my_new_project = None
    for p in projects:
        if projectName==p.name:
            my_new_project=p
            projectID=p.id
            break
    if not my_new_project:
        my_new_project = conn.call('add_project', {'project': {'name': projectName,'description ': 'add pro description'}})
        projectID=my_new_project.id

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

    pd.DataFrame(all_attr_dict.items())

    # -------------------------

    # Create a new template (dataset)
    # This will fail second time around due to a unique naming restriction.
    # You should call 'get_templates' first and update an existing one if one with the same name is already there.

    # 2.1_Datasets&ObjectTypes sheet, look in the Datasets_table
    # DatasetName which is cell A10 in 2.1_Datasets&ObjectTypes sheet

    template = {'name': type_sheet_resourceTypes.values[0][1],'description':'add description here', 'types': []}  # insert the value of the "DatasetName" from excel
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

                if attr_sheet.values[j][6] == 'AttributeSeries':
                    continue # dont upload this attribute to the template. Its used in WaMDaM to keep track of the indiviual attributes
                            # for an array. But Hydra does not have it. Uploading it confused users.

                ObjectType = attr_sheet.values[j][0] #ObjectType
                attr_name = attr_sheet.values[j][1] #AttributeName



                AttributeUnitCV= attr_sheet.values[j][5]

                try:
                    # AttributeUnitCV = attr_sheet.values[j][5]
                    attr_dimension = UnitsTable_df.loc[UnitsTable_df[0]==AttributeUnitCV].iloc[0,1]

                    attr_unit = UnitsTable_df.loc[UnitsTable_df[0]==AttributeUnitCV].iloc[0,2]


                    # attr_dimension = UnitsTable_df.loc[UnitsTable_df[2]==AttributeUnit].iloc[0,1]

                except:
                    msg = "There is a problem with looking up units \n. Invalid Key : {} \n Objectype:{}".format(AttributeUnitCV , ObjectType)
                    raise Exception(msg)
                    # attr_dimension = ''

                # attr_unit=AttributeUnitCV
                # attr_unit=AttributeUnit


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

                mytemplatetype['typeattrs'].append({'type_id': i + 1, 'attr_is_var':True,'attr_id': attr_id,
                                                    'data_type': attr_datatype,
                                                    'unit': attr_unit,
                                                    'properties': {'category': AttributeCategory,'scale':AttributeScale}})
                    # ,
            # --------------------------------------------
            # ,

            # Add some object types to the Template Type  (resource type can be NODE, LINK, GROUP, NETWORK)
        template['types'].append(mytemplatetype)
        # print mytemplatetype

    ## Load the Template name and types to the Hydra db
    tempDB = conn.call('get_templates', {})
    flag_exist_template = False
    for template_item in tempDB:
        if template_item['name'] == template['name']:
            print 'The template already exists in OpenAgua'

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



    # STEP 4: Import WaMDaM Network, Nodes, and links
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    network_sheet = getInstances.GetMasterNetworks(selectedResourceTypeAcro)

    scenario_sheet = getInstances.GetScenarios(selectedResourceTypeAcro, selectedMasterNetworkName)


    for selectedScenarioName in selectedScenarioNames:
        networkName=network_sheet.values[0][0]+'_'+selectedScenarioName

        for templateType in new_template['types']:
            if templateType['resource_type'] == 'NETWORK':
                type_id = templateType['id']
                break


        network_template = {'template':template['name'],'name': networkName, 'description': network_sheet.values[0][4],
                            'project_id': projectID, 'types': [{'id': type_id}]}
        networkName = network_sheet.values[0][0]
        # network_template
        # add_nodes
        # nodes_sheet = wamdam_data['3.2_Nodes']
        nodes_sheet = getInstances.GetNodesByScenario(selectedResourceTypeAcro, selectedMasterNetworkName,selectedScenarioName)

        list_node = []

        node_lookup = {}

        resource_attr_lookup = {}
        dict_res_attr = {}
        type_id = None
        res_id = -1

        # /////make dict_res_attr for network//////////

        network_res_attr = []
        for j in range(len(attr_sheet.values)):
            # if j < 9: continue  # Avoid headers before line 9 in the attribute sheet
            for templateType in new_template['types']:
                if templateType['resource_type'] == 'NETWORK':
                    if attr_sheet.values[j][0] == templateType['name']:
                        name = attr_sheet.values[j][1]
                        AttributeUnitCV = attr_sheet.values[j][5]
                        attr_dimension = UnitsTable_df.loc[UnitsTable_df[0] == AttributeUnitCV].iloc[0, 1]
                        dimension = attr_dimension

                        res_attr = {
                            'ref_key': 'NETWORK',
                            'attr_id': all_attr_dict[(name,dimension)]['id'],
                            'id': res_id,
                        }
                        res_id -= 1
                        # resource_attr_lookup[('NETWORK', res_id)] = res_attr
                        network_res_attr.append(res_attr)
                        dict_res_attr[(networkName, name)] = res_attr
        network_template['attributes'] = network_res_attr
        # ///////////////////////////////////////////////////////////////////////////////////////

        # Iterate over the node instances and assign the parent Object Attributes to each node instance = ResourceAttribute (as in Hydra)
        for i in range(len(nodes_sheet.values)):

            # Look up the type_id in Hydra for each type
            for templateType in new_template['types']:
                if nodes_sheet.values[i][0] == templateType['name']:
                    type_id = templateType['id']
                    break

            if type_id is None:
                raise Exception("Unable to find a type in the template for %s" % nodes_sheet[i][0])

            flag = False
            for node_item in list_node:
                if node_item['name'] == nodes_sheet.values[i][1]:
                    flag = True
            if flag: continue

            description = str(nodes_sheet.values[i][9])
            if description == "None":
                description = ""

            fullname =  nodes_sheet.values[i][1]
            nameShort =  nodes_sheet.values[i][1]



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
                    AttributeUnitCV = attr_sheet.values[j][5]
                    attr_dimension = UnitsTable_df.loc[UnitsTable_df[0] == AttributeUnitCV].iloc[0, 1]
                    dimension =attr_dimension

                    # res_id = (len(list_res_attr) + 1) * -1
                    if (name, dimension) in all_attr_dict.keys():
                        # look up the attribute id on the server based on the both name,dimension together
                        attr_id = all_attr_dict[(name, dimension)]['id']
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

        links_sheet = getInstances.GetLinksByScenario(selectedResourceTypeAcro, selectedMasterNetworkName,selectedScenarioName)

        list_link = []
        type_id = None
        lst_name = []
        for i in range(len(links_sheet)):
            # if i < 8: continue  # Avoid headers before line 9 in the links sheet

            for templateType in new_template['types']:
                if links_sheet.values[i][0] == templateType['name']:
                    type_id = templateType['id']
                    break

            if type_id is None:
                raise Exception("Unable to find a type in the template for %s" % links_sheet.values[i][0])
            description = str(links_sheet.values[i][9])
            if description == "None":
                description = ""

            name = links_sheet.values[i][1]
            fullname = links_sheet.values[i][1]

            if name in lst_name:
                # print name
                continue
            else:
                lst_name.append(name)


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
                    AttributeUnitCV = attr_sheet.values[j][5]
                    attr_dimension = UnitsTable_df.loc[UnitsTable_df[0] == AttributeUnitCV].iloc[0, 1]
                    dimension =attr_dimension

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



        # STEP 5: Import Scenarios and Data Values of Attributes for Nodes and links
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # 5.1 add the scenario
        list_scenario = []
        for i in range(len(scenario_sheet)):
            # only add the selected scenario, one at a time.
            if scenario_sheet.values[i][0] == selectedScenarioName:
                description = str(scenario_sheet.values[i][8])
                if description == "None":
                    description = ""
        ###############################################################################################################

                startdate=scenario_sheet.values[i][4].replace('-', '/')

                try:

                    ScenarioStartDate = datetime.datetime.strptime(str(startdate), "%Y/%m/%d").isoformat()
                except:
                    ScenarioStartDate = startdate.isoformat()

                # get month value from date (either numeric month like 1 or text month like January)
                # we use the value later as a flag to check
                ScenarioStartMonth = datetime.datetime.strptime(ScenarioStartDate, '%Y-%m-%dT%H:%M:%S').month
                print ScenarioStartMonth
        ###############################################################################################################

                enddate=scenario_sheet.values[i][5].replace('-', '/')


                try:
                    ScenarioEndDate = datetime.datetime.strptime(str(enddate), "%Y/%m/%d").isoformat()
                except:
                    ScenarioEndDate = enddate.isoformat()

                TimeStep = str(scenario_sheet.values[i][7])

                scenario = {'name': selectedScenarioName, 'start_time':ScenarioStartDate,'end_time':ScenarioEndDate,'time_step':TimeStep,'description': description, 'resourcescenarios': []}

        # Working with Datasets in Hydra which are equivalent to DataValues tables in WaMDaM
        # http://umwrg.github.io/HydraPlatform/tutorials/webservice/datasets.html?highlight=datasets

        # **************************************************
        # 5.2 Numeric Values
        numerical_sheet = getValuesAll.GetAllNumericValues(selectedResourceTypeAcro, selectedMasterNetworkName,selectedScenarioName)

        list_rs_num = []

        # Iterate over the rows in the Numeric Values sheet [scalars dataset] and associate the value with resource attribute (node instance and attribute)
        for j in range(len(numerical_sheet)):  # //8: reall value row in sheet
            Attr_name = numerical_sheet.values[j][3]
            ObjectType = numerical_sheet.values[j][0]
            Source = numerical_sheet.values[j][4]
            Method = numerical_sheet.values[j][5]


            # look up the dimension using Dataset_attr_Name_Dim based on (attr_name, ObjectType)
            dimension =Dataset_attr_Name_Dim_list[ObjectType, Attr_name]

            if (numerical_sheet.values[j][1], numerical_sheet.values[j][3]) in dict_res_attr.keys():
                rs_num = {'resource_attr_id': dict_res_attr[(numerical_sheet.values[j][1], numerical_sheet.values[j][3])]['id']}
            else:
                raise Exception("Either the node or link names or the attribute provided in the numeric sheet are not defined earlier\n "
                                "Unable to find resource_attr_id in numerical_sheet for %s" % numerical_sheet.values[j][3])



            metadata={'source': Source,'method':Method}


            dataset = {'type': 'scalar', 'name': Attr_name,  'metadata':json.dumps(metadata, ensure_ascii=True),'unit': attr_unit, 'dimension': dimension,
                       'hidden': 'N', 'value': str(numerical_sheet.values[j][6])}
            # The provided dimension here must match the attribute as defined earlier.

            rs_num['value'] = dataset
            list_rs_num.append(rs_num)
        # associate the values, resources attributes to their scenario
        scenario['resourcescenarios'] = list_rs_num
        list_scenario.append(scenario)
        print 'Done with numeric values'


        # network_template['scenarios'] = list_scenario
        # #
        # network = conn.call('add_network', {'net':network_template})

        # ****************************************************
        # 5.3 4_FreeText Values (4_FreeText )
        # Iterate over the rows in the 4_FreeText sheet and associate the value with its scenario, and resource attribute
        Descriptor_sheet = getValuesAll.GetAllTextFree(selectedResourceTypeAcro, selectedMasterNetworkName,selectedScenarioName)
        # Descriptor_sheet = wamdam_data['4_FreeText']

        list_rs_desc=[]
        # Iterate over the rows in the Numeric Values sheet [scalars dataset] and associate the value with resource attribute (node instance and attribute)
        for j in range(len(Descriptor_sheet.values)):
            ObjectType = Descriptor_sheet.values[j][0] #ObjectType
            Attr_name = Descriptor_sheet.values[j][3] #AttributeName
            dimension =Dataset_attr_Name_Dim_list[ObjectType,Attr_name]
            Source = numerical_sheet.values[j][4]
            Method = numerical_sheet.values[j][5]
            metadata = {'source': Source, 'method': Method}

            if (Descriptor_sheet.values[j][1], Descriptor_sheet.values[j][3]) in dict_res_attr.keys():
                rs_desc = {'resource_attr_id': dict_res_attr[(Descriptor_sheet.values[j][1], Descriptor_sheet.values[j][3])]['id']}
            else:
                raise Exception("Either the node or link names or the attribute provided in the free text sheet are not defined earlier\n"
                                "Unable to find resource_attr_id in Free Text sheet for %s" % Descriptor_sheet.values[j][3])

            dataset = {'type': 'descriptor', 'name': Attr_name, 'unit': attr_unit, 'dimension': dimension,
                       'metadata': json.dumps(metadata, ensure_ascii=True),
                       'hidden': 'N', 'value': str(Descriptor_sheet.values[j][6])}
            # print dataset
            # The provided dimension here must match the attribute as defined earlier.

            rs_desc['value'] = dataset
            list_rs_desc.append(rs_desc)
        # associate the values, resources attributes to their scenario

        list_scenario[0]['resourcescenarios'].extend(list_rs_desc)
        print 'Done with Free text'


    # ******************************************************************************************************************

        # 5.7 Seasonal

        # http://umwrg.github.io/HydraPlatform/devdocs/techdocs/timeseries.html?highlight=seasonal#normal-time-series-and-seasonal-time-series

        # SeasonalNumericValues_sheet = wamdam_data['4_SeasonalNumericValues']
        SeasonalNumericValues_sheet = getValuesAll.GetAllSeasonalNumericValues(selectedResourceTypeAcro, selectedMasterNetworkName,selectedScenarioName)

                # add new script here (see time series above)

        seasonal_list = {}
        list_rs_seas=[]
        for k in range(len(SeasonalNumericValues_sheet)):
            attr_name = SeasonalNumericValues_sheet.values[k][3]
            if (SeasonalNumericValues_sheet.values[k][1], attr_name) in seasonal_list.keys():
                seasonal_list[(SeasonalNumericValues_sheet.values[k][1], attr_name)].append(
                    (SeasonalNumericValues_sheet.values[k][7], SeasonalNumericValues_sheet.values[k][8]))
            else:
                values = []
                values.append((SeasonalNumericValues_sheet.values[k][7], SeasonalNumericValues_sheet.values[k][8]))
                seasonal_list[(SeasonalNumericValues_sheet.values[k][1], attr_name)] = values
        # df = pd.DataFrame()
        for key in seasonal_list.keys():
            seasonals = {"Header": {}, "0": {}}
            time_date=''
            for time, value in seasonal_list[key]:
                try:

                    if time == 'October' and ScenarioStartMonth==10:
                        time_date = '9998/10/1'

                    elif time == 'October' and ScenarioStartMonth==1:
                        time_date = '9999/10/1'

                    elif time == 'November' and ScenarioStartMonth==10:
                        time_date = '9998/11/1'

                    elif time == 'November' and ScenarioStartMonth==1:
                        time_date = '9999/11/1'

                    elif time == 'December' and ScenarioStartMonth==10:
                        time_date = '9998/12/1'

                    elif time == 'December' and ScenarioStartMonth==1:
                        time_date = '9999/12/1'

                    elif time == 'January':
                        time_date = '9999/01/1'

                    elif time == 'February':
                        time_date = '9999/02/1'

                    elif time == 'March':
                        time_date = '9999/03/1'

                    elif time == 'April':
                        time_date = '9999/04/1'

                    elif time == 'May':
                        time_date = '9999/05/1'

                    elif time == 'June':
                        time_date = '9999/06/1'

                    elif time == 'July':
                        time_date = '9999/07/1'

                    elif time == 'August':
                        time_date = '9999/08/1'

                    elif time == 'September':
                        time_date = '9999/09/1'

                    t = datetime.datetime.strptime(str(time_date), "%Y/%m/%d").isoformat()
                except:
                    t = time_date.isoformat()
                seasonals["0"][t] = value

            # dimension = all_attr_dict[key[1]]['dimension']
            Attr_name=SeasonalNumericValues_sheet.values[0][3]
            ObjectType = SeasonalNumericValues_sheet.values[0][0]

            dimension = Dataset_attr_Name_Dim_list[ObjectType, Attr_name]
            Source = numerical_sheet.values[j][4]
            Method = numerical_sheet.values[j][5]
            metadata = {'source': Source, 'method': Method}

            if key in dict_res_attr.keys():
                rs_seas = {'resource_attr_id': dict_res_attr[key]['id']}
            else:
                raise Exception("Either the node or link names or the attribute provided in the seasonal sheet are not defined earlier\n"
                                "Unable to find resource_attr_id in seasonal sheet for %s" % key)

            # rs = {'resource_attr_id': all_attr_dict[attr_name]['id']}

            # print 'done with '+ Attr_name
            dataset = {'type': 'timeseries', 'name': Attr_name, 'unit': attr_unit, 'dimension': dimension,
                       'metadata': json.dumps(metadata, ensure_ascii=True),
                       'hidden': 'N', 'value': json.dumps(seasonals)}
            # The provided dimension here must match the attribute as defined earlier.


            rs_seas['value'] = dataset
            list_rs_seas.append(rs_seas)
        # associate the values, resources attributes to their scenario

        list_scenario[0]['resourcescenarios'].extend(list_rs_seas)
        print 'Done with seasonal values'




        # 5.5 Time Series
        # Iterate over the rows in the 4_TimeSeriesValues sheet and associate the value with its scenario, and resource attribute
        # Reference for time series in Hydra: follow this logic
        # http://umwrg.github.io/HydraPlatform/devdocs/techdocs/timeseries.html#an-example-in-python

        # TimeSeriesValues_sheet = wamdam_data['4_TimeSeriesValues']
        TimeSeriesValues_sheet = getValuesAll.GetAllTimeSeriesValues(selectedResourceTypeAcro, selectedMasterNetworkName,selectedScenarioName)


        # Iterate over the rows in the TimeSeriesValues sheet [dataset] and associate the value with resource attribute
        # (node instance and attribute)
        timeseries_list = {}
        list_rs_ts=[]


        for j in range(len(TimeSeriesValues_sheet.values)):
            if not TimeSeriesValues_sheet.values[j][4]:
                continue
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
                if not time:
                    continue
                if value==-9999:
                    value=''
                try:
                    if isinstance(time, datetime.datetime):
                        ts = time.isoformat()
                    else:
                        ts = datetime.datetime.strptime(str(time), "%d/%m/%y").isoformat()
                    timeseries["0"][ts] = value
                except:
                    ts= datetime.datetime.strptime(str(time), "%Y-%m-%d").isoformat()

                    timeseries["0"][ts] = value


            ObjectType = TimeSeriesValues_sheet.values[j][0]
            Attr_name=TimeSeriesValues_sheet.values[j][3]
            dimension = Dataset_attr_Name_Dim_list[ObjectType,Attr_name ]

            Source = TimeSeriesValues_sheet.values[j][6]
            Method = TimeSeriesValues_sheet.values[j][7]

            metadata = {'source': Source, 'method': Method}



            if key in dict_res_attr.keys():
                rs_ts = {'resource_attr_id': dict_res_attr[key]['id']}
            else:
                raise Exception("Either the node or link names or the attribute provided in the time series sheet are not defined earlier\n"
                                "Unable to find resource_attr_id in time series values sheet for %s" % key)


            dataset = {'type': 'timeseries', 'name': Attr_name, 'unit': attr_unit, 'dimension': dimension,
                       'metadata': json.dumps(metadata, ensure_ascii=True),
                       'hidden': 'N', 'value': json.dumps(timeseries)}
            # The provided dimension here must match the attribute as defined earlier.

            rs_ts['value'] = dataset
            list_rs_ts.append(rs_ts)
        # associate the values, resources attributes to their scenario

        list_scenario[0]['resourcescenarios'].extend(list_rs_ts)
        print 'Done with Time Series'


        # ********************************************************
        # 5.6 Arrays
        # Iterate over the rows in the MultiColumns Series sheet and associate the value with its scenario, and resource attribute

        # Reference for arrays in Hydra (not clear to me yet, an example would help)
        #	http://umwrg.github.io/HydraPlatform/tutorials/webservice/datasets.html?highlight=arrays#array-format


        # Will add the array values for each attribute
        # Will add the array values for each attribute
        # Here Column D in excel starting row 19 has the attribute name that for the whole array (its just like the attribute for the descriptor)
        # Columns G, H,....L, etc stwh have the names of the Array "items" or sub-attributes
        # so each value belongs to an Attribute (array name) and a sub-attribute (array item) under an ObjectType and Instance name


        multiAttr_sheet_up_df,multiAttr_sheet_bottom_df = getValuesAll.GetAllMultiAttributeSeries(selectedResourceTypeAcro, selectedMasterNetworkName,selectedScenarioName)


        list_rs_multi = []

        if not multiAttr_sheet_bottom_df.empty:

            subsets = multiAttr_sheet_bottom_df.groupby(['ObjectType', 'InstanceName', 'AttributeName'])

            for subset in subsets.groups.keys():

                dt = subsets.get_group(name=subset)
                ObjectType = dt['ObjectType'].values[0]
                InstanceName = dt['InstanceName'].values[0]
                Attribute_name = dt['AttributeName'].values[0]
                Source = dt['SourceName'].values[0]
                Method =  dt['MethodName'].values[0]
                metadata = {'source': Source, 'method': Method}

                ValuesNumColumns=len(dt.columns)

                Values_df = dt[dt.columns[6:ValuesNumColumns]]
                Values_df = Values_df.dropna(axis = 1, how = 'all')
                templist=Values_df.values.T.tolist()

                if key in dict_res_attr.keys():
                    rs_ts = {'resource_attr_id': dict_res_attr[key]['id']}
                else:
                    raise Exception(
                        "Either the node or link names or the attribute provided in the multicolumns sheet are not defined earlier\n"
                        "Unable to find resource_attr_id in multicolumns values sheet for %s" % key)

                if (InstanceName, Attribute_name) in dict_res_attr.keys():
                    dimension = Dataset_attr_Name_Dim_list[ObjectType, Attribute_name]

                    rs_multi = {'resource_attr_id': dict_res_attr[(InstanceName, Attribute_name)]['id']}




                    dataset = {'type': 'array', 'name':Attribute_name , 'unit': attr_unit,
                               'dimension': dimension,
                               'metadata': json.dumps(metadata, ensure_ascii=True),
                               'hidden': 'N', 'value': json.dumps(templist)}
                    rs_multi['value'] = dataset
                    list_rs_multi.append(rs_multi)


        list_scenario[0]['resourcescenarios'].extend(list_rs_multi)
        print 'Done with multi column arrays'



        network_template['scenarios'] = list_scenario

        network = conn.call('add_network', {'net':network_template})

        print 'successfully uploaded a WaMDaM network and its data to OpenAgua'
