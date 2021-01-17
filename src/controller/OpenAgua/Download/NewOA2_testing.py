import requests
import json


class Hydra(object):
    """
    Example:

    # Set up the class
    hydra = Hydra('https://www.openagua.org/hydra', api_key=os.environ['OPENAGUA_SECRET_KEY'])

    # Method 1: hydra.call(function, **kwargs)
    resp1 = hydra.call('get_project', project_id=123)

    # Method 2: hydra.func_name(**kwargs)
    resp2 = hydra.get_project(project_id=123)

    """

    username = None
    password = None

    def __init__(self, endpoint_url, username='', password=None, api_key=None):
        self.key = api_key

        if endpoint_url[-1] != '/':
            endpoint_url += '/'
        self.endpoint = endpoint_url

        self.username = username
        self.password = password or api_key

    def call(self, func, dict_kwargs=None, **kwargs):
        if dict_kwargs is not None:
            return self._call(func, **dict_kwargs)
        else:
            return self._call(func, **kwargs)

    def _call(self, func, *args, **kwargs):
        payload = {}
        if args:
            payload['args'] = list(args)
            payload['kwargs'] = kwargs
        else:
            payload = kwargs
        endpoint = self.endpoint + func
        resp = requests.post(endpoint, auth=(self.username, self.password), json=payload)
        try:
            return json.loads(resp.content.decode())
        except:
            return resp.content.decode()

    def __getattr__(self, name):
        def method(*args, **kwargs):
            if name == 'call':
                return self._call(*args, **kwargs)
            else:
                return self._call(name, *args, **kwargs)

        return method


if __name__ == '__main__':
    import os

    # Set up the hydra class
    endpoint = 'https://www.openagua.org/api/v1/hydra'
    # # api_key = os.environ['iF1Txy.8oF92MkasvN1eq0nP9xJVbH6kYqdN4YPM']
    #
    username='amabdallah@aggiemail.usu.edu'
    password=''
    hydra = Hydra(endpoint, username=username,password=password)

    # project={'name':projectName,'description':'add pro description'}

    # attr = {'attr':{'name': 'Test', 'dimension_id': '1'}}
    # Networks_call={'project_id': '1937', 'include_values': 'N'}

    # add_attr = hydra._call('add_attribute',{'attr':{'name': 'Test', 'dimension_id': '10'}})
    #
    # print(add_attr)
    # my_new_project = hydra._call('add_project', {'name': 'tes12', 'description ': 'add pro description'})
    # my_new_pro = hydra._call('add_attribute', {'name': 'tes12', 'dimension_id': '10'})

    # add = hydra._call('get_dimensions')
    # print(add)
    # server_attr = hydra.call('get_attribute_by_name_and_dimension', {'name': 'tes12', 'dimension_id': 10})
    # server_attr_id=server_attr['id']
    #
    # server_dimensions = hydra.call('get_dimensions')

    # for server_dimension in server_dimensions:
    #     if server_dimension['name']==attr_dimension
    #         server_dimension_id=server_dimension['id']

    # print (server_dimensions)

    scenario = hydra._call('get_scenario', 3461)

    # add the call here with static values for testing

    # scenario={'layout': {'class': 'uncertainty'},   'description': 'Scenario',
    #                                                           'network_id': 1444, 'parent_id': 3434,
    #                                                           'id': 3456, 'name': 'abc'}
    scenario['parent_id']=3460
    result = hydra._call('update_scenario', scenario)


    print result
