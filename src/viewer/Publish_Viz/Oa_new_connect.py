import requests
import json
import os

class Hydra(object):
    """
    Example:

    # Set up the class
    hydra = Hydra('https://www.openagua.org/api/v1/hydra/', api_key=os.environ['OPENAGUA_SECRET_KEY'])

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

    # Set up the class
    endpoint = 'https://www.openagua.org/api/v1/hydra/'
    # endpoint = 'http://127.0.0.1:5000/hydra'
    # api_key = os.environ['iF1Txy.8oF92MkasvN1eq0nP9xJVbH6kYqdN4YPM']
    # hydra = Hydra(endpoint, api_key=api_key)

    # Method 1: hydra.call(function, **kwargs)
    # project1 = hydra.call('get_all_resource_data', {'scenario_id': 2484,'include_metadata': 'Y'})
    # print(project1)

    # # Method 2: hydra.func_name(**kwargs)
    # project2 = hydra.get_project(project_id=1201)
    # print('Successfully retrieved {}'.format(project2['name']))
    #
    # # Method 3: hydra.func_name(*args)
    # project3 = hydra.get_project(1201)
    # print('Successfully retrieved {}'.format(project3['name']))
