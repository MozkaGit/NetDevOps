#! /usr/local/bin/python3.9
import requests
import json
import time

login_url = 'http://10.154.0.19/api/auth/login'
cred = '{"username":"admin","password":"eve","html5":"-1"}'
headers = {'Accept': 'application/json'}

login = requests.post(url=login_url, data=cred)
cookies = login.cookies
print(cookies)

####### Stop all Nodes
url = "http://10.154.0.19/api/labs/Test%20-%20Network%20Automation%20Routing.unl/nodes/stop"
start_api = requests.get(url,cookies=cookies)
response = start_api.json()

if start_api.status_code == 200:
    print("All nodes have shut down correctly.")
    print(start_api.text)
else:
    print("Nodes shutdown failure. Status Code:", start_api.status_code)

time.sleep(3)

####### Delete all Nodes
url_berlin = "http://10.154.0.19/api/labs/Test%20-%20Network%20Automation%20Routing.unl/nodes/1"
delete_berlin = requests.delete(url=url_berlin,cookies=cookies)
response = delete_berlin.json()

if delete_berlin.status_code == 200:
    print("Berlin router has been correctly deleted.")
    print(response)
else:
    print("Node deletion failure. Status Code:", delete_berlin.status_code)

url_paris = "http://10.154.0.19/api/labs/Test%20-%20Network%20Automation%20Routing.unl/nodes/2"
delete_paris = requests.delete(url=url_paris,cookies=cookies)
response = delete_paris.json()

if delete_paris.status_code == 200:
    print("Paris router has been correctly deleted.")
    print(response)
else:
    print("Node deletion failure. Status Code:", delete_paris.status_code)

time.sleep(1)

###### Delete Topology
lab_url = 'http://10.154.0.19/api/labs/Test%20-%20Network%20Automation%20Routing.unl'
delete_api = requests.delete(url=lab_url,cookies=cookies)
response = delete_api.json()

if delete_api.status_code == 200:
    print("The topology has been correctly deleted.")
    print(response)
else:
    print("Topology deletion failure. Status Code:", delete_api.status_code)

