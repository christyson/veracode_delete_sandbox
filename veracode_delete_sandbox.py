import sys
import requests
import argparse
from lxml import etree
import datetime as dt
from dateutil.parser import parse
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py import VeracodeAPI

#api_base = "https://api.veracode.com/appsec/v1"
api_target = "https://analysiscenter.veracode.com/api/5.0/deletesandbox.do"
headers = {"User-Agent": "Python HMAC Example"}

def main():

    parser = argparse.ArgumentParser(
        description='This script deletes a Sandbox if you have appropriate permissions - Note: this is not undoable')
    parser.add_argument('-a', '--app', help='App name to delete sandbox in',required=True)
    parser.add_argument('-s', '--sandbox', default="", help='Sandbox name to delete',required=True)
    args = parser.parse_args()

    data = VeracodeAPI().get_app_list()
    results = etree.fromstring(data)
    found = False
    for app in results:
        if (app.attrib["app_name"] == args.app) and (args.sandbox != ""):
           sandbox_list=VeracodeAPI().get_sandbox_list(app.attrib["app_id"])
           sandboxes = etree.fromstring(sandbox_list)
           for sandbox in sandboxes:
              if sandbox.attrib["sandbox_name"] == args.sandbox:
                 found = True
                 try:
                    response = requests.get(api_target, auth=RequestsAuthPluginVeracodeHMAC(), headers={"User-Agent": "api.py"},params={'sandbox_id': sandbox.attrib["sandbox_id"]})
                 except requests.RequestException as e:
                    print("Error occured")
                    print(e)
                    sys.exit(1)

                 if response.ok:
                    print("Sandbox deleted")
                 else:
                    print(response.status_code)                 
                 exit(0)
              else:
                 print ('Sandbox: '+args.sandbox+' of app: '+args.app+' not found!')
                 exit(1)
    if (not found):
       print ('App: '+args.app+' with sandbox: '+args.sandbox+' does not exist')
    exit(0)

if __name__ == '__main__':
    main()