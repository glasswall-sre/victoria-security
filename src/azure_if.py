from azure.graphrbac import GraphRbacManagementClient
from azure.common.credentials import ServicePrincipalCredentials
import adal, requests

class AzureIF:
    @staticmethod 
    def __call_azure_active_directory(url, token):
        headers = {
            'Content-Type' : 'application\json',
            'Authorization': 'Bearer {}'.format(token)
        }
        r = requests.get(url, headers=headers)
        return r.json()
        
    @staticmethod
    def __get_token(secrets):
        url = 'https://login.microsoftonline.com/glasswallsolutions.com/oauth2/v2.0/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': secrets["CLIENT_ID"],
            'scope': 'https://graph.microsoft.com/.default',
            'client_secret': secrets["CLIENT_SECRET"]
        }
        r = requests.post(url, data=data)
        return r.json().get('access_token')

    @staticmethod
    def __get_ad_sre_group(secrets):
        token = AzureIF.__get_token(secrets)
        url = f"https://graph.microsoft.com/v1.0/groups/{secrets['SRE_TEAM_AD_GROUP_OBJECT_ID']}/members"
        result = AzureIF.__call_azure_active_directory(url, token)
        return result['value']

    @staticmethod
    def is_user_in_ad_filtered(target_email, secrets):
        token = AzureIF.__get_token(secrets)
        url = f"https://graph.microsoft.com/v1.0/users?$filter=startswith(mail,'{target_email}')"
        result = AzureIF.__call_azure_active_directory(url, token)
        return True if len(result['value']) >= 1 else False

    @staticmethod
    def is_user_in_sre_ad_group(target_email, secrets):
        for sre_member in AzureIF.__get_ad_sre_group(secrets):
            if target_email == sre_member['mail']:
                return True
        return False