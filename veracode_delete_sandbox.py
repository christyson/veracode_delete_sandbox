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
    parser.add_argument('-a', '--app', help='App name to delete sandbox in',required=False)
    parser.add_argument('-s', '--sandbox', default="", help='Sandbox name to delete',required=False)
    parser.add_argument('-y', '--year', default="", help='year',required=False)
    parser.add_argument('-m', '--month', default="", help='month',required=False)
    parser.add_argument('-d', '--day', default="", help='day',required=False)

    args = parser.parse_args()
    data = VeracodeAPI().get_app_list()
    results = etree.fromstring(data)
    found = False
    for app in results:
        print ("app: " + app.attrib["app_name"])
        if (app.attrib["app_name"] == args.app):
           sandbox_list=VeracodeAPI().get_sandbox_list(app.attrib["app_id"])
           sandboxes = etree.fromstring(sandbox_list)
           print('sandbox: ' + args.sandbox)
           print('year: ' + args.year)
           for sandbox in sandboxes:
              print ('Sandbox: ' + sandbox.attrib["sandbox_name"] + ', date: '  + sandbox.attrib["last_modified"])
              lastModifiedDate = dt.datetime.strptime(sandbox.attrib["last_modified"], '%Y-%m-%dT%H:%M:%S%z')
              if args.sandbox != '' and sandbox.attrib["sandbox_name"] == args.sandbox:
                 print('found sandbox name ' + args.sandbox)
                 found = True
                 remove_sandbox(sandbox)
              elif args.year != '' and lastModifiedDate.year == int(args.year):
                  print('found year ' + args.year)
                  deletefile = True
                  if args.month != '' and lastModifiedDate.month != int(args.month):
                     print('month did not match')
                     deletefile = False
                  if args.day != '' and lastModifiedDate.day != int(args.day):
                     print('day did not match')
                     deletefile = False
                  if deletefile == True:
                   found = True
                   remove_sandbox(sandbox)
              else:
                 print ('Sandbox: '+args.sandbox+' of app: '+args.app+' not found!')
                 exit(1)
    if (not found):
       print ('App: '+args.app+' with sandbox: '+args.sandbox+' does not exist')
    exit(1)

def remove_sandbox(sandbox):
   try:
      response = requests.get(api_target, verify=False, auth=RequestsAuthPluginVeracodeHMAC(), headers={"User-Agent": "api.py"},params={'sandbox_id': sandbox.attrib["sandbox_id"]})
   except requests.RequestException as e:
      print("Error occurred")
      print(e)
      sys.exit(1)

   if response.ok:
      print("Sandbox deleted " + sandbox.attrib["sandbox_name"])
   #   exit(0)
   else:
      print(response.status_code)                 
      exit(1)

if __name__ == '__main__':
    main()
