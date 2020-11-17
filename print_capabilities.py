#!/usr/bin/env python3

import sys
try:
    import requests
except ImportError as ie:
    print(ie)
    sys.exit("Please install python-requests!")
import urllib3
import json
from mysecrets import mysecrets

# Modify the mysecrets.py
fqdn = mysecrets["fqdn"]
username = mysecrets["username"]
password = mysecrets["password"]
validate_https_certificate = mysecrets["validate_https_certificate"]
# This will not work directly, as the params have to be urlencoded
#login_url = "https://{0}/?domain=auth&username={1}&password={2}".format(fqdn, username, password)
omniswitch_url = "https://{0}/".format(fqdn)

login_params = {
    "domain":"auth",
    "username":username,
    "password":password
}

req_headers = {
    "Accept":"application/vnd.alcatellucentaos+json",
    "ALU_CONTEXT":"vrf=default"
}

if(validate_https_certificate.lower() == "yes"):
    check_certs = True
else:
    # This is needed to get rid of a warning coming from urllib3 on self-signed certificates
    # print("[!] Ignoring certificate warnings or self-signed certificates!")
    # print("[!] You should really fix this!")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    check_certs = False    

# req will also hold a session cookie for all following interactions
req = requests.Session()

# Login and obtain cookie for session
resp = req.get(omniswitch_url, params=login_params, headers=req_headers, verify=check_certs)
if resp.status_code == 200:
    # resp.json() will contain something like {'result': {'domain': 'auth (login)', 'diag': 200, 'error': '', 'output': '', 'data': []}}
    if resp.json()["result"]["diag"] == 400:
        sys.exit(resp.json()["result"]["error"])
    elif resp.json()["result"]["diag"] == 200:
        pass
    else:
        sys.exit("Something went wrong: {0}".format(resp.json()))

getwebview_params = {
    "domain":"callFunction",
    "function":"getWebviewInformation" 
}

resp = req.get(omniswitch_url, params=getwebview_params, headers=req_headers, verify=check_certs)
if resp.status_code == 200:
    # resp.json() will contain something like {'result': {'domain': 'auth (login)', 'diag': 200, 'error': '', 'output': '', 'data': []}}
    if resp.json()["result"]["diag"] == 400:
        sys.exit(resp.json()["result"]["error"])
    elif resp.json()["result"]["diag"] == 200:
        for k, v in resp.json()["result"]["data"].items():
            if isinstance(v, str):
                print(v)
            elif isinstance(v, dict):
                print(json.dumps(v, indent=4, sort_keys=True))
    else:
        sys.exit("Something went wrong: {0}".format(resp.json()))