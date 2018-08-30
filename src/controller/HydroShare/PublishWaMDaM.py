#!/usr/bin/python
 # -*- coding: utf-8 -*-

import json
import define
from hs_restclient import HydroShare, HydroShareAuthBasic
import pandas as pd

from controller.wamdamAPI.GetSQLiteContentMetadata import GetSQLiteContentMetadata


#import the C:\Wizard1.3Beta\src\controller\wamdamAPI\GetSQLiteContentMetadata.py to here
# from


def publishOnHydraShare(userName, password, filePathOfSqlite):
    auth = HydroShareAuthBasic(username=userName, password=password)
    hs = HydroShare(auth=auth)

    # We Import the classes from ConnectDB_ParseExcel.py. These classes are inherited by LoadMetaData
    # from ..ConnectDB_ParseExcel import *

    ### 4. Creating a new HydroShare resource

    # The best way to save your data is to put it back into HydroShare
    # and is done using the `createHydroShareResource` function.
    # The first step is to identify the files you want to save to a HydroShare.
    #  The cell below lists all the files in the current working directory.
    #
    # define HydroShare required metadata
    title = 'Test resourceNew'
    abstract = 'This a test for runing a use case of wamdam using jupyter in HydroShare'

    keywords = ['WaMDaM', 'Systems models','water management']


    # set the resource type that will be created.
    resource_type = 'CompositeResource'

    # metadata={"coverages": {"type":"box", "value":{'north: 50, south: 30, east: 40, west: 20'}}}

    # metadata={"coverages":[{"type": "period", "value": {"start": "01/01/2000", "end": "12/12/2010"}}]}
    # metadata={"coverages":'[{"type": "period", "value": {"start": "01/01/2000", "end": "12/12/2010"}}]'}

    # WaMDaMSQLite='BearRiverDatasets_Jan2018.sqlite'

    # create a list of files that will be added to the HydroShare resource.

    # files = [hs.content['BearRiverDatasets_Jan2018.sqlite'], 'WaMDaM_Use_Case2.1.ipynb']  # this notebook

    # files = [hs.content['BearRiverDatasets_Jan2018.sqlite'], 'WaMDaM_Use_Case2.1.ipynb']  # this notebook

    # metadata=
    # extra_metadata={}
    # extra_metadata=json.dumps({'ObjectTypes':'Reservoir'})

    # extra_metadata=json.dumps({"ObjectTypes":[{"asd":"Reservoir" ,"dfszdfsd":"John Smith"}]})
    # {'ObjectTypes':'Reservoir'})
    control_meta = GetSQLiteContentMetadata()

    CVObjectTypes_Result_df = control_meta.GetCVObjectTypes()
    Key=CVObjectTypes_Result_df.keys()
    CVObjectTypes_Result_List=','.join(CVObjectTypes_Result_df[Key[0]].values)

    extra_metadata=json.dumps({'ObjectTypes': CVObjectTypes_Result_List})
    #
    # result like this
    #
    # Reservoir, Demand sites, Canal, River


    # extra_metadata=json.dumps({'ObjectTypes': 'Reservoir, Demand sites, Canal, River'})

    # coverageaa={'coverage':{'type': 'period', 'start': '01/01/2000', 'end': '12/12/2010'}}


    # extra_metadata=json.dumps({
    #             "title":"Great Salt Lake Level and Volume",
    #             "creators":[
    #                         {"name":"John Smith","description":"/user/24/","organization":"USU","email":"john.smith@usu.edu","address":"Engineering Building, USU, Logan, Utah","phone":"435-789-9087","homepage":"","order":1},
    #                         {"name":"Lisa Miller","description":"","organization":"","email":"","address":"","phone":"","homepage":"","order":2}
    #                        ]})


                               # "creators":[{"name":"John Smith","description":"/user/24/","organization":"USU","email":"john.smith@usu.edu","address":"Engineering Building, USU, Logan, Utah","phone":"435-789-9087","homepage":"","order":1}
    # ]})

    # print metadata
    # "name":"Lisa Miller","description":"","organization":"","email":"","address":"","phone":"","homepage":"","order":2}
    # ]}
    # """

    # get the path to the SQLite connection
    # nodes.csv
    # resource_file=
    # http://hs-restclient.readthedocs.io/en/latest/hs_restclient.html#module-hs_restclient

    # create the new resource
    # resource_file= get the path to the sqlite file that the Wizard is connected to
    # resource_file
    # resource_file – a read-only binary file-like object (i.e. opened with the flag ‘rb’)
    # or a string representing path to file to be uploaded as part of the new resource
    SqliteName = define.dbName
    # this line uploads the new WaMdaM resource to HydroShare
    NewRes=hs.createResource(resource_type, title=title, resource_file=filePathOfSqlite, resource_filename=SqliteName, abstract=abstract, keywords=keywords,
                      edit_users=None, view_users=None, edit_groups=None, view_groups=None, metadata=None,
                      extra_metadata=extra_metadata, progress_callback=None)

    return NewRes

# publishOnHydraShare('dd', 'dd', 'dd')