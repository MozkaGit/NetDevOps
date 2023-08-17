#! /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11
import requests
import json

login_url = 'http://10.154.0.12/api/auth/login'
credentials = '{"username":"admin","password":"eve","html5":"-1"}'
headers = {'Accept': 'application/json'}

login = requests.post(url=login_url, data=credentials)
cookies = login.cookies
print(cookies)

lab_url = 'http://10.154.0.12/api/labs/test-env.unl'
delete_api = requests.delete(url=lab_url,cookies=cookies)
response = delete_api.json()
print(response)