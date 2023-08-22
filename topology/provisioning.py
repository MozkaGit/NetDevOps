#! /usr/local/Python_envs/Python3/bin/python3

import requests
import json
import re
import time
from telnetlib import Telnet

login_url = 'http://10.154.0.12/api/auth/login'
cred = '{"username":"admin","password":"eve","html5":"-1"}'
headers = {'Accept': 'application/json'}
login = requests.post(url=login_url, data=cred)
cookies = login.cookies
print(cookies)

# Labs
lab_url = "http://10.154.0.12/api/labs"
lab_data = {
    "path": "/",
    "name": "Test - Network Automation Routing",
    "version": "1",
    "author": "MozkaGit",
    "description": "Test environment before deploying configurations in Production"
}

lab_data = json.dumps(lab_data)
lab_api = requests.post(url=lab_url,data=lab_data,cookies=cookies,headers=headers)
response = lab_api.json()
print(response)

# Create Cloud Network for management by Ansible
network_url = "http://10.154.0.12/api/labs/Test%20-%20Network%20Automation%20Routing.unl/networks"
network_data = {
    "count": "1",
    "visibility": "1",
    "name": "MGMT",
    "type": "pnet1",
    "left": "873",
    "top": "591",
    "postfix": 0
}

network_data = json.dumps(network_data)
network_api = requests.post(url=network_url,data=network_data,cookies=cookies,headers=headers)
response = network_api.json()
print(response)

# Create Bridge Network for interconnection between nodes
network_url = "http://10.154.0.12/api/labs/Test%20-%20Network%20Automation%20Routing.unl/networks"
network_data = {
    "count": "1",
    "visibility": "1",
    "name": "Bridge",
    "type": "bridge",
    "left": "873",
    "top": "258",
    "postfix": 0
}

network_data = json.dumps(network_data)
network_api = requests.post(url=network_url,data=network_data,cookies=cookies,headers=headers)
response = network_api.json()
print(response)

def create_instance(name):
    instances = []

    ios_data = {
        "template": "iol",
        "type": "iol",
        "count": "1",
        "image": "i86bi-linux-l3-adventerprisek9-15.5.2T.bin",
        "name": name,
        "icon": "Router.png",
        "nvram": "1024",
        "ram": "1024",
        "ethernet": "1",
        "serial": "0",
        "config": "0",
        "delay": "0",
        "left": "1042",
        "top": "273",
        "postfix": 0
    }

    ios_data = json.dumps(ios_data)
    create_url = 'http://10.154.0.12/api/labs/Test%20-%20Network%20Automation%20Routing.unl/nodes'

    create_api = requests.post(url=create_url, data=ios_data, cookies=cookies, headers=headers)
    response = create_api.json()
    print(response)
    device_id = response['data']['id']
    print(f"Created Instance ID is: {device_id}")

    instances.append(device_id)

    # Interface connection to MGMT
    print("Connecting the Interface")
    add_int_url = f'http://10.154.0.12/api/labs/Test%20-%20Network%20Automation%20Routing.unl/nodes/{device_id}/interfaces'
    int_map = '{"0":"1"}'
    connect_int = requests.put(url=add_int_url, data=int_map, headers=headers, cookies=cookies)
    print(connect_int.json())
    
    # Interface connection between Paris and Berlin
    print("Connecting the Interface")
    add_int_url = 'http://10.154.0.12/api/labs/Test%20-%20Network%20Automation%20Routing.unl/nodes/1/interfaces'
    int_map = '{"16":2}'
    connect_int = requests.put(url=add_int_url, data=int_map, headers=headers, cookies=cookies)
    print(connect_int.json())
    
    print("Connecting the Interface")
    add_int_url = 'http://10.154.0.12/api/labs/Test%20-%20Network%20Automation%20Routing.unl/nodes/2/interfaces'
    int_map = '{"16":2}'
    connect_int = requests.put(url=add_int_url, data=int_map, headers=headers, cookies=cookies)
    print(connect_int.json())

    # Start Instance
    print("Starting the Device")
    url = f"http://10.154.0.12/api/labs/Test%20-%20Network%20Automation%20Routing.unl/nodes/{device_id}/start"
    start_api = requests.request("GET", url, headers=headers, cookies=cookies)
    print(start_api.json())

    # Get telnet Port
    url = f"http://10.154.0.12/api/labs/Test%20-%20Network%20Automation%20Routing.unl/nodes"
    nodes = requests.get(url=url, headers=headers, cookies=cookies)
    data = nodes.json()
    node_dict = data['data']
    port_details = node_dict[f"{device_id}"]['url']
    port_pattern = re.compile(r'telnet.+:(\d+)')
    port_output = int((port_pattern.search(port_details).group(1)))
    return port_output

def telnet_initial(telnet_port):
    TELNET_TIMEOUT = 10
    tn = Telnet(host='10.154.0.12', port=telnet_port, timeout=TELNET_TIMEOUT)
    tn.write(b"\n")
    tn.write(b"\n")
    tn.write(b"\n")
    tn.write(b"no\n")
    time.sleep(10)
    tn.write(b"\n")
    
def device_config(device_name,telnet_port):
	TELNET_TIMEOUT = 10
	tn = Telnet(host='10.154.0.12', port=telnet_port, timeout=TELNET_TIMEOUT)
	with open(f"topology/startup_cfg/{device_name}.ios", 'r') as cmd_file:
		for cmd in cmd_file.readlines():
			cmd = cmd.strip('\r\n')
			tn.write(cmd.encode()+ b'\r')
			time.sleep(1)

def provision(device_names):
    for device_name in device_names:
        telnet_port = create_instance(device_name)
        print(f"Telnet Port of the Node is: {telnet_port}")
        print("Initiating sleep for 100s")
        time.sleep(100)
        print("Finished sleep for 100s")
        telnet_initial(telnet_port)
        print("Finished Initial Configuration")
        time.sleep(15)
        device_config(device_name,telnet_port)
        print("Finished Setting up the device")


# Noms des instances à créer
device_names = ["Router-Berlin", "Router-Paris"]

provision(device_names)
