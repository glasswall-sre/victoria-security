from azure.graphrbac import GraphRbacManagementClient
from azure.common.credentials import ServicePrincipalCredentials
import adal, requests
from typing import Dict, List


def __get_azure_ad(url : str, token):
    """Make a GET request inserting the required headers

    Args:
        url: url to make get request to
        token: token obtained from __get_token()

    Returns:
        json response
    """
    headers = {
        'Content-Type' : 'application\json',
        'Authorization': 'Bearer {}'.format(token)
    }
    r = requests.get(url, headers=headers)
    return r.json()
    

def __get_token(secrets : Dict) -> str:
    """Make a POST request to get an Azure Token in order to call other Azure APIs

    Args:
        secrets: The secrets read from secrets.get_secrets()

    Returns:
        token : str
    """
    url = 'https://login.microsoftonline.com/glasswallsolutions.com/oauth2/v2.0/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': secrets["CLIENT_ID"],
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': secrets["CLIENT_SECRET"]
    }
    r = requests.post(url, data=data)
    return r.json().get('access_token')


def __get_ad_sre_group(secrets) -> List:
    """Obtain SRE Group Members

    Args:
        secrets: The secrets read from secrets.get_secrets()

    Returns:
        List of members apart of SRE Team
    """
    token = __get_token(secrets)
    url = f"https://graph.microsoft.com/v1.0/groups/{secrets['SRE_TEAM_AD_GROUP_OBJECT_ID']}/members"
    result = __get_azure_ad(url, token)
    return result['value']


def is_user_in_ad_filtered(target_email : str, secrets : Dict) -> bool:
    """Verify the target_email is within Azure AD

    Args:
        target_email: url to make get request to
        secrets: The secrets read from secrets.get_secrets()

    Returns:
        True if email exists within the Azure AD subscription
        False if otherwise
    """
    token = __get_token(secrets)
    url = f"https://graph.microsoft.com/v1.0/users?$filter=startswith(mail,'{target_email}')"
    result = __get_azure_ad(url, token)
    return len(result['value']) > 0


def is_user_in_sre_ad_group(target_email : str, secrets : Dict) -> bool:
    """Verify the target_email is witin the Azure AD SRE Group

    Args:
        target_email: email to search in the SRE Group
        secrets: The secrets read from secrets.get_secrets()

    Returns:
        True if target_email is in SRE Group.
        False if it could not find in SRE Group.
    """
    for sre_member in __get_ad_sre_group(secrets):
        if target_email == sre_member['mail']:
            return True
    return False