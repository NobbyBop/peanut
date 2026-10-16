import requests
import json
def hit_endpoint(endpoint, method, body):
    if method == "POST":
        resp = requests.post(endpoint, data=json.loads(body))
        return resp
    elif method == "GET":
        resp = requests.get(endpoint, data=json.loads(body))
        return resp
    else:
        return "Invalid method."