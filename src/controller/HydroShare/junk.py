
import json
import define
from hs_restclient import HydroShare, HydroShareAuthBasic

extra_metadata = json.dumps({'ObjectTypes': 'Reservoir, Demand sites, Canal, River'},{'Methods': 'Reservoir, Demand sites, Canal, River'},ensure_ascii=False)
# extra_metadata.append({'Methods': 'Reservoir, Demand sites, Canal, River'})

print extra_metadata