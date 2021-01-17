from hs_restclient import HydroShare, HydroShareAuthBasic
import json

username = 'amabdallah'

# username = 'adelabdallah'

password = ''

auth = HydroShareAuthBasic(username=username, password=password)

hs = HydroShare(auth=auth)

resource_type = 'CompositeResource'

abstract = 'My abstract'

title = 'new tes5255t'

keywords = ('my keyword 1', 'my keyword 2')
rtype = 'CompositeResource'

fpath = 'C:\Users\Rosenberg\Desktop\Ecosystem/WASH3.sqlite'

metadata = '[{"coverage":{"type":"period", "value":{"start":"01/01/2000", "end":"12/12/2010"}}}, {"creator":{"name":"John Smith"}}, {"creator":{"name":"Lisa Miller"}}]'


resource_id = hs.createResource(resource_type, title, resource_file=fpath, keywords=keywords, abstract=abstract,
                                metadata=metadata)

SqliteName='WASH3.sqlite'

params = {}

params['temporal_coverage'] = {"start": '2000', "end": '2003'}

params['title'] = SqliteName

params['spatial_coverage'] = {
    "type": "box",

    "units": "Decimal degrees",

    "eastlimit": float(-110.8200),  # -110.8200,

    "northlimit": float(42.8480),  # 42.8480,

    "southlimit": float(40.7120),  # 40.7120,

    "westlimit": float(-113.0000),  # -113.0000,

    "name": "12232",

    "projection": "WGS 84 EPSG:4326"
}

# add metadata to the SQLite file
options = {"file_path": SqliteName, "hs_file_type": "SingleFile"}
# print options

result = hs.resource(resource_id).functions.set_file_type(options)



spatial = hs.resource(resource_id).files.metadata(SqliteName, params)