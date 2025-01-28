"""
Get the network IDs of an organisation. Supply the organisation ID that can be found at
https://dashboard.meraki.com/api/v1/organizations 
"""
import os
import meraki
from dotenv import load_dotenv

#Loads the .env file 
load_dotenv() 

#Pull variables from the .env file
API_KEY = os.getenv('API_KEY')
ORG_ID = os.getenv('ORG_ID')

#Create Meraki dashboard client
dashboard = meraki.DashboardAPI(
    API_KEY,
    suppress_logging=True
    )

#To get thr organisation ID, browse to https://dashboard.meraki.com/api/v1/organizations and find the correct org
organization_id = ORG_ID

#Send Request to get all networks from the organization
response = dashboard.organizations.getOrganizationNetworks(
    organization_id, total_pages='all'
)

#Loop through the response to pull all the IDs from each network in the organisation
network_ids = []
for network in response:
    network_ids.append(network['id'])

for network in network_ids:
    print(network)


