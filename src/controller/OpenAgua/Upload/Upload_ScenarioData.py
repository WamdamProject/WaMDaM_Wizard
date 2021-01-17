

import datetime
import json

# Import Scenario from WaMDaM SQLite using the API
from controller.wamdamAPI.GetResourceStructure import GetResourceStructure
from controller.wamdamAPI.GetMetadataByScenario import GetMetadataByScenario

from controller.wamdamAPI.GetInstancesByScenario import GetInstancesBySenario
from controller.wamdamAPI.GetAllValuesByScenario import GetAllValuesByScenario
from controller.wamdamAPI.GetUnitCVs import GetUnits

from controller.OpenAgua.Download.NewOA2 import Hydra_OA
from collections import OrderedDict


# General library for working with JSON objects
import json
# Used for working with files.
import os, sys, datetime

import logging

def PrepareScenarioData(selectedResourceTypeAcro, selectedMasterNetworkName,selectedScenarioNames,scenario_sheet,dict_res_attr,
                        Dataset_attr_Name_Dim_list,Dataset_attr_Name_Dim_unit,HydraUnits):
    getValuesAll = GetAllValuesByScenario()

    list_scenario = []
    # STEP 5: Import Scenarios and Data Values of Attributes for Nodes and links
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



    print 'reading and preparing scenarios'
    # 5.1 add the scenario
    for jjj ,selectedScenarioName in enumerate(selectedScenarioNames):
        for i in range(len(scenario_sheet)):
            # only add the selected scenario, one at a time.
            if scenario_sheet.values[i][0] == selectedScenarioName:
                print 'prepare data to the ' + selectedScenarioName + ' scenario'


                if scenario_sheet.values[i][9]:
                    description = scenario_sheet.values[i][9].encode('utf-8')
                    if description == "None":
                        description = ""
                ###############################################################################################################

                startdate =str(scenario_sheet.values[i][4]) #.replace('-', '/')

                try:

                    ScenarioStartDate = datetime.datetime.strptime(startdate, "%Y-%m-%d").isoformat()
                except:
                    ScenarioStartDate = startdate.isoformat()

                # get month value from date (either numeric month like 1 or text month like January)
                # we use the value later as a flag to check
                ScenarioStartMonth = datetime.datetime.strptime(ScenarioStartDate, '%Y-%m-%dT%H:%M:%S').month

                print ScenarioStartMonth
                ###############################################################################################################

                enddate =str(scenario_sheet.values[i][5]) #.replace('-', '/')


                try:
                    ScenarioEndDate = datetime.datetime.strptime(enddate, "%Y-%m-%d").isoformat()
                except:
                    ScenarioEndDate = enddate.isoformat()
                # ScenarioType =''
                TimeStep = str(scenario_sheet.values[i][7])


                ScenarioParent = scenario_sheet.values[i][8].lower()

                ScenarioType=scenario_sheet.values[i][9].lower()

                if ScenarioType=='': #or ScenarioType=='results':
                    ScenarioType='scenario'


                scenario = {'name': selectedScenarioName,
                            'start_time' :startdate,
                            'end_time' :enddate ,
                            'time_step' :TimeStep,
                            'layout': {
                                'class': ScenarioType,
                                'parent':''
                                        },
                            'description': description,
                            'resourcescenarios': []}


                # 1. Use unit ID (use the Hydra units tabel and their Ids
                # 2. Check again on start and end dates of the scenario for WEAP and WASH. Download both to WaMDaM.
                # 3. see how the download works for October water year.
                # 4. Finish HydroShare upload


                # Working with Datasets in Hydra which are equivalent to DataValues tables in WaMDaM
                # http://umwrg.github.io/HydraPlatform/tutorials/webservice/datasets.html?highlight=datasets

                # **************************************************
                # 5.2 Numeric Values
                numerical_sheet = getValuesAll.GetAllNumericValues(selectedResourceTypeAcro, selectedMasterNetworkName
                                                                   ,selectedScenarioName)

                list_rs_num = []

                # Iterate over the rows in the Numeric Values sheet [scalars dataset] and associate the value with resource attribute (node instance and attribute)
                # if not numerical_sheet:
                #     print "empty numerical_sheet"
                #     continue
                for j in range(len(numerical_sheet)):  # //8: reall value row in sheet
                    Attr_name = numerical_sheet.values[j][3]
                    ObjectType = numerical_sheet.values[j][0]
                    Source = numerical_sheet.values[j][4]
                    Method = numerical_sheet.values[j][5]


                    # look up the dimension using Dataset_attr_Name_Dim based on (attr_name, ObjectType)
                    dimension =Dataset_attr_Name_Dim_list[ObjectType, Attr_name]

                    if (numerical_sheet.values[j][1], numerical_sheet.values[j][3]) in dict_res_attr.keys():

                        rs_num = {
                            'resource_attr_id': dict_res_attr[(numerical_sheet.values[j][1], numerical_sheet.values[j][3])][
                                'id']}
                    else:
                        raise Exception(
                            "Either the node or link names or the attribute provided in the numeric sheet are not defined earlier\n "
                            "Unable to find resource_attr_id in numerical_sheet for %s" % numerical_sheet.values[j][3])

                    metadata = {'source': Source, 'method': Method}
                    attr_unit = Dataset_attr_Name_Dim_unit[(ObjectType,Attr_name)]

                    # Get the unit_id from the Hydra server
                    for uni in HydraUnits:
                        if uni['name'] == attr_unit:
                            unit_id = uni['id']
                        # else:
                        #     print "this unit does not exist in Hydra"
                        #     print  attr_unit

                    dataset = {'type': 'scalar', 'name': Attr_name, 'metadata': metadata,'unit_id':unit_id,
                               # 'unit': attr_unit, 'dimension': dimension,
                               'hidden': 'N', 'value': str(numerical_sheet.values[j][6])}

                    # The provided dimension here must match the attribute as defined earlier.

                    rs_num['dataset'] = dataset
                    list_rs_num.append(rs_num)
                # associate the values, resources attributes to their scenario

                scenario['resourcescenarios'] = list_rs_num


                list_scenario.append(scenario) # test

                print 'Done with numeric values. Next is Free Text'

                # ****************************************************
                # 5.3 4_FreeText Values (4_FreeText )
                # Iterate over the rows in the 4_FreeText sheet and associate the value with its scenario, and resource attribute
                Descriptor_sheet = getValuesAll.GetAllTextFree(selectedResourceTypeAcro, selectedMasterNetworkName,
                                                               selectedScenarioName)
                # Descriptor_sheet = wamdam_data['4_FreeText']

                list_rs_desc = []
                # Iterate over the rows in the Numeric Values sheet [scalars dataset] and associate the value with resource attribute (node instance and attribute)

                # if not Descriptor_sheet:
                #     print "empty numerical_sheet"
                #     continue
                for j in range(len(Descriptor_sheet.values)):
                    ObjectType = Descriptor_sheet.values[j][0]  # ObjectType
                    Attr_name = Descriptor_sheet.values[j][3]  # AttributeName
                    dimension = Dataset_attr_Name_Dim_list[ObjectType, Attr_name]
                    Source = Descriptor_sheet.values[j][4]
                    Method = Descriptor_sheet.values[j][5]
                    metadata = {'source': Source, 'method': Method}
                    attr_unit = Dataset_attr_Name_Dim_unit[(ObjectType, Attr_name)]

                    if (Descriptor_sheet.values[j][1], Descriptor_sheet.values[j][3]) in dict_res_attr.keys():
                        rs_desc = {'resource_attr_id':
                                       dict_res_attr[(Descriptor_sheet.values[j][1], Descriptor_sheet.values[j][3])]['id']}
                    else:
                        raise Exception(
                            "Either the node or link names or the attribute provided in the free text sheet are not defined earlier\n"
                            "Unable to find resource_attr_id in Free Text sheet for %s" % Descriptor_sheet.values[j][3])

                    # Get the unit_id from the Hydra server
                    for uni in HydraUnits:
                        if uni['name'] == attr_unit:
                            unit_id = uni['id']

                    dataset = {'type': 'descriptor', 'name': Attr_name,'unit_id':unit_id,
                               # 'unit': attr_unit, 'dimension': dimension,
                               'metadata': json.dumps(metadata, ensure_ascii=True),
                               'hidden': 'N', 'value': str(Descriptor_sheet.values[j][6])}
                    # print dataset
                    # The provided dimension here must match the attribute as defined earlier.

                    rs_desc['dataset'] = dataset
                    list_rs_desc.append(rs_desc)
                # associate the values, resources attributes to their scenario

                list_scenario[len(list_scenario) - 1]['resourcescenarios'].extend(list_rs_desc)

                print 'Done with Free text. Next, is seasonal data'

                # ******************************************************************************************************************

                # 5.7 Seasonal

                # http://umwrg.github.io/HydraPlatform/devdocs/techdocs/timeseries.html?highlight=seasonal#normal-time-series-and-seasonal-time-series

                # SeasonalNumericValues_sheet = wamdam_data['4_SeasonalNumericValues']
                SeasonalNumericValues_sheet = getValuesAll.GetAllSeasonalNumericValues(selectedResourceTypeAcro,
                                                                                       selectedMasterNetworkName,
                                                                                       selectedScenarioName)

                # add new script here (see time series above)

                seasonal_list = {}
                list_rs_seas = []
                # if not SeasonalNumericValues_sheet:
                #     print "empty SeasonalNumericValues_sheet"
                #     continue

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

                    # seasonals = OrderedDict()
                    seasonals = {"0": {}}
                    time_date = ''
                    for time, value in seasonal_list[key]:
                        try:
                            # if time == 'October' and ScenarioStartMonth == 10:
                            #     time_date = '9998/10/1'
                            #
                            # elif time == 'October' and ScenarioStartMonth == 1:
                            #     time_date = '9999/10/1'
                            #
                            # elif time == 'November' and ScenarioStartMonth == 10:
                            #     time_date = '9998/11/1'
                            #
                            # elif time == 'November' and ScenarioStartMonth == 1:
                            #     time_date = '9999/11/1'
                            #
                            # elif time == 'December' and ScenarioStartMonth == 10:
                            #     time_date = '9998/12/1'
                            #
                            # elif time == 'December' and ScenarioStartMonth == 1:
                            #     time_date = '9999/12/1'

                            if time == 'October':
                                time_date = '9999/10/1'

                            elif time == 'November':
                                time_date = '9999/11/1'

                            elif time == 'December' :
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
                        if value=='':
                            value=0
                        seasonals["0"][t] = value

                    # dimension = all_attr_dict[key[1]]['dimension']
                    Attr_name = SeasonalNumericValues_sheet.values[0][3]
                    ObjectType = SeasonalNumericValues_sheet.values[0][0]

                    dimension = Dataset_attr_Name_Dim_list[ObjectType, Attr_name]
                    Source = SeasonalNumericValues_sheet.values[k][4]
                    Method = SeasonalNumericValues_sheet.values[k][5]
                    metadata = {'source': Source, 'method': Method}
                    attr_unit = Dataset_attr_Name_Dim_unit[(ObjectType, Attr_name)]

                    if key in dict_res_attr.keys():
                        rs_seas = {'resource_attr_id': dict_res_attr[key]['id']}
                    else:
                        raise Exception(
                            "Either the node or link names or the attribute provided in the seasonal sheet are not defined earlier\n"
                            "Unable to find resource_attr_id in seasonal sheet for %s" % key)

                    # Get the unit_id from the Hydra server
                    for uni in HydraUnits:
                        if uni['name'] == attr_unit:
                            unit_id = uni['id']

                    # rs = {'resource_attr_id': all_attr_dict[attr_name]['id']}

                    # print 'done with '+ Attr_name
                    dataset = {'type': 'timeseries', 'name': Attr_name,'unit_id':unit_id,
                               # 'unit': attr_unit, 'dimension': dimension,
                               'metadata': json.dumps(metadata, ensure_ascii=True),
                               'hidden': 'N', 'value': json.dumps(seasonals)}
                    # The provided dimension here must match the attribute as defined earlier.

                    rs_seas['dataset'] = dataset
                    list_rs_seas.append(rs_seas)
                # associate the values, resources attributes to their scenario

                list_scenario[len(list_scenario) - 1]['resourcescenarios'].extend(list_rs_seas)

                print 'Done with seasonal values. Next is time series data'

                # 5.5 Time Series
                # Iterate over the rows in the 4_TimeSeriesValues sheet and associate the value with its scenario, and resource attribute
                # Reference for time series in Hydra: follow this logic
                # http://umwrg.github.io/HydraPlatform/devdocs/techdocs/timeseries.html#an-example-in-python

                # TimeSeriesValues_sheet = wamdam_data['4_TimeSeriesValues']
                TimeSeriesValues_sheet = getValuesAll.GetAllTimeSeriesValues(selectedResourceTypeAcro,
                                                                             selectedMasterNetworkName,
                                                                             selectedScenarioName)

                # Iterate over the rows in the TimeSeriesValues sheet [dataset] and associate the value with resource attribute
                # (node instance and attribute)
                timeseries_list = {}
                list_rs_ts = []

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
                    timeseries = { "0": {}}
                    for time, value in timeseries_list[key]:
                        if not time:
                            continue
                        if value == -9999 or value == '-9999.00000' or value == '-9999' or value == -9999.0:
                            value = ''
                        try:
                            if isinstance(time, datetime.datetime):
                                ts = time.isoformat()
                            else:
                                ts = datetime.datetime.strptime(str(time), "%d/%m/%y").isoformat()
                            timeseries["0"][ts] = value
                        except:
                            ts = datetime.datetime.strptime(str(time), "%Y-%m-%d").isoformat()

                            timeseries["0"][ts] = value

                    ObjectType = TimeSeriesValues_sheet.values[j][0]
                    Attr_name = TimeSeriesValues_sheet.values[j][3]
                    dimension = Dataset_attr_Name_Dim_list[ObjectType, Attr_name]

                    Source = TimeSeriesValues_sheet.values[j][6]
                    Method = TimeSeriesValues_sheet.values[j][7]

                    metadata = {'source': Source, 'method': Method}
                    attr_unit = Dataset_attr_Name_Dim_unit[(ObjectType, Attr_name)]

                    if key in dict_res_attr.keys():
                        rs_ts = {'resource_attr_id': dict_res_attr[key]['id']}
                    else:
                        raise Exception(
                            "Either the node or link names or the attribute provided in the time series sheet are not defined earlier\n"
                            "Unable to find resource_attr_id in time series values sheet for %s" % key)

                    # Get the unit_id from the Hydra server
                    for uni in HydraUnits:
                        if uni['name'] == attr_unit:
                            unit_id = uni['id']



                    dataset = {'type': 'timeseries', 'name': Attr_name,'unit_id':unit_id,
                               # 'unit': attr_unit, 'dimension': dimension,
                               'metadata': json.dumps(metadata, ensure_ascii=True),
                               'hidden': 'N', 'value': json.dumps(timeseries)}
                    # The provided dimension here must match the attribute as defined earlier.

                    rs_ts['dataset'] = dataset
                    list_rs_ts.append(rs_ts)
                    # print 'Done with Time Series for ' + Attr_name +'_' +ObjectType
                # associate the values, resources attributes to their scenario

                list_scenario[len(list_scenario) - 1]['resourcescenarios'].extend(list_rs_ts)

                print 'Done with Time Series. Next is multi attribute data'

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

                multiAttr_sheet_up_df, multiAttr_sheet_bottom_df = getValuesAll.GetAllMultiAttributeSeries(
                    selectedResourceTypeAcro, selectedMasterNetworkName, selectedScenarioName)

                list_rs_multi = []

                if not multiAttr_sheet_bottom_df.empty:

                    subsets = multiAttr_sheet_bottom_df.groupby(['ObjectType', 'InstanceName', 'AttributeName'])

                    for subset in subsets.groups.keys():

                        dt = subsets.get_group(name=subset)
                        ObjectType = dt['ObjectType'].values[0]
                        InstanceName = dt['InstanceName'].values[0]
                        Attribute_name = dt['AttributeName'].values[0]
                        Source = dt['SourceName'].values[0]
                        Method = dt['MethodName'].values[0]
                        metadata = {'source': Source, 'method': Method}
                        attr_unit = Dataset_attr_Name_Dim_unit[(ObjectType, Attribute_name)]

                        ValuesNumColumns = len(dt.columns)

                        Values_df = dt[dt.columns[6:ValuesNumColumns]]
                        Values_df = Values_df.dropna(axis=1, how='all')
                        templist = Values_df.values.T.tolist()

                        if key in dict_res_attr.keys():
                            rs_ts = {'resource_attr_id': dict_res_attr[key]['id']}
                        else:
                            raise Exception(
                                "Either the node or link names or the attribute provided in the multicolumns sheet are not defined earlier\n"
                                "Unable to find resource_attr_id in multicolumns values sheet for %s" % key)

                        if (InstanceName, Attribute_name) in dict_res_attr.keys():
                            dimension = Dataset_attr_Name_Dim_list[ObjectType, Attribute_name]

                            rs_multi = {'resource_attr_id': dict_res_attr[(InstanceName, Attribute_name)]['id']}

                            # Get the unit_id from the Hydra server
                            for uni in HydraUnits:
                                if uni['name'] == attr_unit:
                                    unit_id = uni['id']


                            dataset = {'type': 'array', 'name': Attribute_name,'unit_id':unit_id,
                                       # 'unit': attr_unit,'dimension': dimension,
                                       'metadata': json.dumps(metadata, ensure_ascii=True),
                                       'hidden': 'N', 'value': json.dumps(templist)}
                            rs_multi['dataset'] = dataset
                            list_rs_multi.append(rs_multi)

                list_scenario[len(list_scenario) - 1]['resourcescenarios'].extend(list_rs_multi)
                print 'Done with multi column arrays.'
    return list_scenario