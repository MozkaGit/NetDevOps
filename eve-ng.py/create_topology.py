#! /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11
import requests
import json

login_url = 'http://10.154.0.12/api/auth/login'
credentials = '{"username":"admin","password":"eve","html5":"-1"}'
headers = {'Accept': 'application/json'}

# Create Lab
login = requests.post(url=login_url, data=credentials)
cookies = login.cookies
print(cookies)

lab_data = {"path":"/","name":"test-env","version":"1","author":"MozkaGit","description":"Test environment for CI/CD pipeline"}

lab_data = json.dumps(lab_data)
lab_url = 'http://10.154.0.12/api/labs'

lab_api = requests.post(url=lab_url, data=lab_data, cookies=cookies, headers=headers)
response = lab_api.json()
print(response)

# Create Nodes
def create_instance(total):
    login = requests.post(url=login_url, data=credentials)
    cookies = login.cookies
    print(cookies)
    for i in range(1,total+1):

        ios_data = {"template":"iol","type":"iol","count":"1","image":"i86bi-linux-l3-adventerprisek9-15.5.2T.bin","name":f"R_{i}","icon":"Router.png","nvram":"1024","ram":"1024","ethernet":"1","serial":"0","config":"0","delay":"0","left":"600","top":"219", "postfix":0}

        ios_data = json.dumps(ios_data)
        create_url = 'http://10.154.0.12/api/labs/test-env.unl/nodes'

        create_api = requests.post(url=create_url, data=ios_data, cookies=cookies, headers=headers)
        response = create_api.json()
        print(response)
        device_id = response['data']['id']
        print(f"Created Instance is: {device_id}")

total_instance = int(input("Enter total number of Instances Required:"))
create_instance(total_instance)


# Create Network
login = requests.post(url=login_url, data=credentials)
cookies = login.cookies
print(cookies)

cloud_data = {"count":"1","visibility":"1","name":"MGMT","type":"pnet1","left":"676","top":"330","postfix":0}

cloud_data = json.dumps(cloud_data)
cloud_url = 'http://10.154.0.12/api/labs/test-env.unl/networks'

cloud_api = requests.post(url=cloud_url, data=cloud_data, cookies=cookies, headers=headers)
response = cloud_api.json()
print(response)