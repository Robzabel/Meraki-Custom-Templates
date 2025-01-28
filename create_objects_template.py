"""
Create network objects for use with firewalls. Currently not in Meraki library so need to use requests module. You will need to provide 
an xlsx spreadsheet with 2 columns (Name, Subnet) - note the capital letters for the column names
"""
import os
import requests
import datetime
import json
import pandas as pd
from dotenv import load_dotenv


############################################ Declare Variables #####################################################
#Load the .env file 
load_dotenv() #Load the .env file 

#Pull values from the .env file
API_KEY = os.getenv('API_KEY')
FILE = os.getenv('OBJECTS_FP')
ORG_ID = os.getenv('ORG_ID')

#Supply the URL of the Meraki API
url = f"https://api.meraki.com/api/v1/organizations/{ORG_ID}/policyObjects"

#Provide headers for authentication and formatting 
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": f"{API_KEY}"
}

#open spreadsheet, take value columns and convert into a list 
spread_sheet = pd.read_excel(f'{FILE}')
name = spread_sheet['Name'].tolist()
subnet = spread_sheet['Subnet'].tolist()

#create list to hold any errored APs
not_found=[]

############################################ Send the Requests #####################################################
#Loop through the dictionary from the spreadsheet and add them to MEraki
for name, subnet in zip(name, subnet):
    #try update the Meraki with the device details
    try:
        #Convert the payload to JSON 
        payload = json.dumps({"name": name, "type" : "cidr", "category" : "network", "cidr" : subnet})
        #Send the request
        response = requests.request('POST', url, headers=headers, data = payload)

    #Catch any errors when uploading & add them to the list of not_found    
    except Exception as error:
        print(f"{error}{name}")
        not_found.append(name)
    continue

########################################### Responses & Records ####################################################
#When the script finishes, print the devices that were not created in the portal to the terminal and a file 
if not_found:
    print("The Following devices were not created in the portal:")
    [print(x) for x in not_found]
    with open (f"Devices_not_created_{datetime.date.today()}.txt", 'w') as file:
        file.write(f"{[x for x in not_found]}")
else:
    print("All devices successfully uploaded")