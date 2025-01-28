"""
Get a JSON list of all policy objects
"""
import os
import requests
import json
from dotenv import load_dotenv

#Load the .env file 
load_dotenv() #Load the .env file 

#Pull API key from the .env file
API_KEY = os.getenv('API_KEY')
ORG_ID = os.getenv('ORG_ID')

#Supply the URL of the Meraki API
url = f"https://api.meraki.com/api/v1/organizations/{ORG_ID}/policyObjects"

#Provide headers for authentication and formatting 
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": f"{API_KEY}"
}

#Not a POST request so no payload 
payload = None

#Send the request with the custom headers/data
response = requests.request('GET', url, headers=headers, data = payload)

#print the response
print(response.text)