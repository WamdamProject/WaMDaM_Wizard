#!/usr/bin/python
 # -*- coding: utf-8 -*-

import define
from hs_restclient import HydroShare, HydroShareAuthBasic

import pandas as pd

from controller.wamdamAPI.GetSQLiteContentMetadata import GetSQLiteContentMetadata
import json




def publishOnHydraShare(userName, password, filePathOfSqlite, title, abstract, author):
    auth = HydroShareAuthBasic(username=userName, password=password)
    hs = HydroShare(auth=auth)
    # hs = HydroShare(auth=auth, hostname='beta.hydroshare.org')
    hs = HydroShare(auth=auth, hostname='hydroshare.org')

    # We Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
    # from ..ConnectDB_ParseExcel import *

    ### 4. Creating a new HydroShare resource

    # The best way to save your data is to put it back into HydroShare
    # and is done using the `createHydroShareResource` function.
    # The first step is to identify the files you want to save to a HydroShare.
    #  The cell below lists all the files in the current working directory.
    #
    # define HydroShare required metadata
    title = title
    abstract = abstract

    keywords = ['WaMDaM', 'Systems models','water management']


    # set the resource type that will be created.
    resource_type = 'CompositeResource'


    control_meta = GetSQLiteContentMetadata()

    ResourceTypes_Result_df=control_meta.GetResourceTypes()
    CVObjectTypes_Result_df = control_meta.GetCVObjectTypes()
    CVAttributes_Result_df=control_meta.GetCVAttributes()
    MasterNetworks_Result_df=control_meta.GetMasterNetworks()
    Scenarios_Result_df_Result=control_meta.GetScenarios()
    Sources_Result_df_Result=control_meta.GetSources()
    Methods_Result_df_Result=control_meta.GetMethods()
    People_Result_df_Result=control_meta.GetPeople()
    Organizations_Result_df_Result=control_meta.GetOrganizations()

    East_Longitude_value, West_Longitude_value, South_Latitude_value, North_Latitude_value=control_meta.GetSpatialCoverage()

    start_value,end_value=control_meta.GetTemporalCoverage()


    Key=CVObjectTypes_Result_df.keys()

    ResourceTypes_Result_df_List=', '.join(ResourceTypes_Result_df[Key[0]].values)
    CVObjectTypes_Result_List=', '.join(CVObjectTypes_Result_df[Key[0]].values)
    CVAttributes_Result_df_List=', '.join(CVAttributes_Result_df[Key[0]].values)
    MasterNetworks_Result_df_List=', '.join(MasterNetworks_Result_df[Key[0]].values)
    Scenarios_Result_df_List=', '.join(Scenarios_Result_df_Result[Key[0]].values)
    Sources_Result_df_List=', '.join(Sources_Result_df_Result[Key[0]].values)
    Methods_Result_df_List=', '.join(Methods_Result_df_Result[Key[0]].values)
    People_Result_df_List=', '.join(People_Result_df_Result[Key[0]].values)
    Organizations_Result_df_List=', '.join(Organizations_Result_df_Result[Key[0]].values)

    East_Longitude_value_string=', '.join(map(str, East_Longitude_value[0]))
    West_Longitude_value_string=', '.join(map(str, West_Longitude_value[0]))
    South_Latitude_value_string=', '.join(map(str, South_Latitude_value[0]))
    North_Latitude_value_string=', '.join(map(str, North_Latitude_value[0]))

    start_value_date=', '.join(map(str, start_value[0]))
    end_value_date=', '.join(map(str, end_value[0]))


    extra_metadata=json.dumps({'ResourceTypes': ResourceTypes_Result_df_List,
                               'ObjectTypesCV': CVObjectTypes_Result_List,
                               'AttributesCV': CVAttributes_Result_df_List,
                               'MasterNetworkName': MasterNetworks_Result_df_List,
                               'Scenarios': Scenarios_Result_df_List,
                               'Souces': Sources_Result_df_List,
                               'Methods': Methods_Result_df_List,
                               'People': People_Result_df_List,
                               'Organizations': Organizations_Result_df_List

                               })
    # creator=Author

    metadata = [{"coverage":{"type":"period", "value":{"start":start_value_date, "end":end_value_date}}}]

    authors = author.split(';')
    for auth in authors:
        auth_data = {"creator": {"name": auth}}
        metadata.append(auth_data)

    metadata = json.dumps(metadata)

    SqliteName = define.dbName

    params = {}



    params['temporal_coverage'] = {"start": start_value_date, "end": end_value_date}
    params['title'] = SqliteName

    # get the path to the SQLite connection
    # nodes.csv
    # resource_file=
    # http://hs-restclient.readthedocs.io/en/latest/hs_restclient.html#module-hs_restclient

    # create the new resource
    # resource_file= get the path to the sqlite file that the Wizard is connected to
    # resource_file
    # resource_file – a read-only binary file-like object (i.e. opened with the flag ‘rb’)
    # or a string representing path to file to be uploaded as part of the new resource
    # this line uploads the new WaMdaM resource to HydroShare



    print SqliteName

    resource_id=hs.createResource(resource_type, title=title, resource_file=filePathOfSqlite, resource_filename=SqliteName, abstract=abstract, keywords=keywords,
                      edit_users=None, view_users=None, edit_groups=None, view_groups=None, metadata=metadata,
                      extra_metadata=extra_metadata, progress_callback=None)

    print resource_id
    options = {"file_path": SqliteName, "hs_file_type": "SingleFile"}
    print options

    result = hs.resource(resource_id).functions.set_file_type(options)


    file = ""
    for f in hs.resource(resource_id).files.all():
        file += f.decode('utf8')

    file_json = json.loads(file)
    file_id = file_json["results"][0]["id"]
    print file_id



    params['spatial_coverage'] = {

        "type": "box",

        "units": "Decimal degrees",

        "eastlimit": float(East_Longitude_value_string),  # -110.8200,

        "northlimit": float(North_Latitude_value_string),  # 42.8480,

        "southlimit": float(South_Latitude_value_string),  # 40.7120,

        "westlimit": float(West_Longitude_value_string),  # -113.0000,

        "name": "12232",

        "projection": "WGS 84 EPSG:4326"

    }


    spatial=hs.resource(resource_id).files.metadata(file_id, params)

    print 'Done'
    print resource_id
    return resource_id,file_id,params,hs

