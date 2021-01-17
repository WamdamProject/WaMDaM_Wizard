
import requests
import json


url = 'https://www.openagua.org/api/v1/hydra/{rpc}'
# api_key = 'iF1Txy.8oF92MkasvN1eq0nP9xJVbH6kYqdN4YPM'
api_key = 'OApass1'
username_oa='amabdallah@aggiemail.usu.edu'
projectName='test'

def hydra_call(self, func, dict_kwargs=None, **kwargs):
    if dict_kwargs is not None:
        return self._call(func, **dict_kwargs)
    else:
        return self._call(func, **kwargs)
def _call(self, func, *args, **kwargs):
    payload = {}
    if args:
        payload['args'] = list(args)
    payload['kwargs'] = kwargs
    endpoint = self.endpoint + func
    resp = requests.post(endpoint, auth=(self.username, self.password), json=payload)
    try:
        return json.loads(resp.content.decode())
    except:
        return resp.content.decode()
    payload = {}
    if args:
        payload['args'] = list(args)
    payload['kwargs'] = kwargs
    endpoint = self.endpoint + func


def hydra_call(username, password, func, *args, **kwargs):
    payload=dict(args=list(args),kwargs=kwargs)

    endpoint = url.format(rpc=func)
    resp = requests.post(endpoint, auth=(username, password), json=payload) #specificy kwargs and args
    try:
        return json.loads(resp.content.decode())
    except:
        return resp.content.decode()

project={'name':projectName,'description':'add pro description'}

my_new_project = hydra_call(username_oa, api_key,'add_project',(project,))

print (my_new_project)

# projectID = my_new_project['id']

# example 1
# network = hydra_call('get_network', network_id=123)

# example 2
# network = hydra_call('get_network', {'network_id': 1150})

# print (network)
#
# rep=requests.post('https://www.openagua.org/hydra/get_network', auth=('', 'eD1D8u.kmEhbGApc9HZSS1GHzaT6WGwoVVjSRlXg'), json={'network_id': 77})
#
# print (rep.content)

# projects = hydra_call('get_projects', {})
# #
# print (projects)

# requests.post('https://www.openagua.org/hydra/get_projects', auth=('', 'MY_API_KEY'), json={})

# GetNetworks_metadata = hydra_call('get_networks', {'project_id': 1940, 'include_values': 'N'})
#
# print (GetNetworks_metadata)

# projects = hydra_call('get_projects', {})
# requests.post('https://www.openagua.org/hydra/get_projects', auth=('', 'MY_API_KEY'), json={})

# Get_scenarios_metadata = hydra_call('get_scenarios', {'network_id': 1168, 'include_values': 'N'})
#
# print (Get_scenarios_metadata)