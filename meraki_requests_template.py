"""
Basic template for sending a request and priniting the response
"""
import os
import meraki
import json
from dotenv import load_dotenv

#Loads the .env file
load_dotenv()  

#Pull API key from the .env file
API_KEY = os.getenv('API_KEY')

#Create Meraki dashboard client
dashboard = meraki.DashboardAPI(
    API_KEY,
    suppress_logging=True
    )

#Send Request
response = dashboard.organizations.getOrganizations()


print(json.dumps(response))