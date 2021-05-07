#%%
# from azure.common.credentials import ServicePrincipalCredentials
from azure.core import credentials
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
import time


#%%
from configparser import ConfigParser

parser = ConfigParser()
parser.read('datafactory.ini')
print(parser)

subscriptionid = parser.get('azureconfig', 'subscriptionid')
clientid = parser.get('azureconfig', 'clientid')
secret = parser.get('azureconfig', 'secret')
tenantid = parser.get('azureconfig', 'tenantid')


adfname = parser.get('datafactory','adfname')
rgname = parser.get('datafactory','rgname')
# %%
# credentials = ServicePrincipalCredentials(
cred = ClientSecretCredential(
    client_id=clientid,
    client_secret=secret,
    tenant_id=tenantid
)

adf_client = DataFactoryManagementClient(
    credential=cred,
    subscription_id=subscriptionid)
# %%
rg_params = {'location' : 'australiaeast'}
df_params = {'location' : 'australiaeast'}
adf_resource =Factory(location='australiaeast')
adf = adf_client.factories.create_or_update(
    factory_name=adfname,
    resource_group_name=rgname,
    factory=adf_resource
)
# %%
print(adf)
while adf.provisioning_state != 'Succeeded':
    adf = adf_client.factories.get(rgname, adfname)
    time.sleep(1)
# %%
