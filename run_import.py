#!/usr/bin/env python3

# Imports
import pyvii
import time
import process_file
import configparser

CONF = configparser.ConfigParser()

# Read in properties file
try:
    CONF.read("config.props")
except IOError as e:
    print('File %s not found!' % e)

# Create Authentication Header for SOAP Request
authheader = {
    'url': CONF.get("Auth Header", "url"),
    'Domain': CONF.get("Auth Header", "domain"),
    'userid': CONF.get("Auth Header", "userid"),
    'userpassword': CONF.get("Auth Header", "userpassword"),
    'oemid': CONF.get("Auth Header", "oemid"),
    'oempassword': CONF.get("Auth Header", "oempassword")
}

# Read in other configuration parameters.
inputfilename = CONF.get("Config", "inputfilename")
organizationid = CONF.get("Config", "organizationid")
importdefinitionid = CONF.get("Config", "importdefinitionid")

def run_import(organizationid, importdefinitionid):
    try:
        api = pyvii.Api(authheader)
        # print(api.organization_query_root())
        print(api.import_create(organizationid, importdefinitionid, 'extract_out_%s.csv'  % time.strftime("%Y%m%d")))
    except pyvii.APIError as e:
        print(e.message.fault)

def main():
    # Process extract file from Fusion prior to importing into profiles
    process_file.process_file(inputfilename)
    # Sleeping process to ensure file has been created.
    print('Sleeping 10 seconds for file creation')
    for i in range(10,0,-1):
        time.sleep(1)
        print(i)
    run_import(organizationid, importdefinitionid)

if __name__ == '__main__':
    main()
