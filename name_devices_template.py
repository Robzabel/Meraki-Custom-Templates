"""
Name devices based off their serial numbers. Add the device names and serial numbers to a C.S.V. file
along with the address of the company then run the script. Dont need to specify the organisation as
the Serial numbers are unique.
"""
import os
import meraki
import pandas as pd
from dotenv import load_dotenv
import datetime

#Loads the .env file 
load_dotenv() 

#Pull API key from the .env file
API_KEY = os.getenv('API_KEY')

#Create Meraki dashboard client
dashboard = meraki.DashboardAPI(
    API_KEY,
    suppress_logging=True
    )

#open spreadsheet and grab variables (Check File Path)
df = pd.read_excel('path/to/file')
serial = df['Serial'].tolist()
name = df['NAME'].tolist()
address = df['address'].tolist()
tags = df['tags'].tolist()

#create list to hold any errored APs
not_found=[]

#Loop through the dictionary from the spreadsheet and add them to MEraki
for serial, name, address in zip(serial, name, address):
    #try update the Meraki with the device details
    try:
        response = dashboard.devices.updateDevice(
        serial = serial, 
        name = name, 
        address = address
        )
    #Catch any errors when uploading & add them to the list of not_found    
    except Exception as error:
        print(f"{error}{address}")
        not_found.append(name)
    continue

#When the script finishes, print the devices that were not created in the portal to the terminal and a file 
if not not_found:
    print("All devices successfully uploaded")
else:
    print("The Following devices were not created in the portal:")
    [print(x) for x in not_found]
    with open (f"Devices_not_created_{datetime.date.today()}.txt", 'w') as file:
        file.write(f"{[x for x in not_found]}")
