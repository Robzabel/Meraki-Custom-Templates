"""
Supply the organisation ID and the script will gather all the WAN uplin IP addresses
"""
import os
import meraki
import pandas as pd
from dotenv import load_dotenv

###################################### Declare Function  ###################################
def network_name(dashboard, network_ids):
    """
    Takes the dashboard API and a list of network IDs to retun the names of the networks
    """
    network_name = []
    for network_id in network_ids:
        response = dashboard.networks.getNetwork(
            network_id
        )
        network_name.append(response.get('name'))
    return(network_name)

###########################################Setup Variables #################################
#Loads the .env file
load_dotenv()  

#Pull keys from the .env file
API_KEY = os.getenv('API_KEY')
ORG_ID = os.getenv('ORG_ID')

#Create Meraki dashboard client
dashboard = meraki.DashboardAPI(
    API_KEY,
    suppress_logging=True
    )

#Send Request to get Organisation info
response = dashboard.organizations.getOrganizationUplinksStatuses(
    ORG_ID, total_pages='all'
)
#####################################Get the network Names #####################################

network_ids = []
for network in response:
    network_ids.append(network['networkId'])

names =network_name(dashboard, network_ids)

#################################set index & Column titles ######################################

column_title = ["Network", "WAN 1 ", " WAN 2", "Notes"]
index = len(response)

###################################### IP Addresses ##############################################

ip_addresses = []
for location in response:
    uplinks = []
    for i in range(len(location['uplinks'])):
        ip = uplinks.append(location['uplinks'][i]['publicIp'])
    ip_addresses.append(uplinks)


######################################Export to Excel ############################################

full_list = []
for i in range(len(names)):
    ip_addresses[i].insert(0, names[i])

df = pd.DataFrame(ip_addresses ,  columns=column_title)

df.to_excel('pandas_to_excel.xlsx', sheet_name='new_sheet_name')
    