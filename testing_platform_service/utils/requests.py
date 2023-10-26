import requests, json


def http_request(url, method, headers = None, params = None,files = None):
    response = None
    if method.lower() == 'get':
        response = requests.get(url=url, headers=headers,params=params)
    elif  method.lower() == 'post':
        if files:
            response = requests.post(url=url, headers=headers, files=files)
        else:
            response = requests.post(url=url, headers=headers, data=params)
    elif method.lower() == 'put':
        response = requests.put(url=url, headers=headers, data=params)
    elif method.lower() == 'delete':
        response = requests.delete(url=url, headers=headers, data=params)
    return response