import slackbot_authentication.azure_ad as azure_ad
import slackbot_authentication.slack_utils as slack_utils
from slackbot_authentication.authorisation_query import is_user_allowed
from typing import Dict

class AuthenticationRules:
    @staticmethod
    def run(message, slack_email : str, secrets : Dict) -> Dict:
        # Verify Slack Token is Valid and existant in request
        if not slack_utils.is_valid_slack_verification_token(message.token, secrets):
            return {
                'statusCode': 401,
                'body': "Unauthorized: Invalid Token, Request suspected not coming from Slack"
            }

        # Verify User is in Glasswall Azure Active Directory
        if not azure_ad.is_user_in_ad_filtered(slack_email, secrets):
            return {
                'statusCode': 401,
                'body': "Unauthorized: Slack User is not in Azure Active Directory"
            }

        # Verify User is from SRE Group Not-General function
        if not azure_ad.is_user_in_sre_ad_group( slack_email, secrets ):
            return {
                'statusCode': 401,
                'body': "Unauthorized: Slack User is not in Azure Active Directory Group (SRE Team)"
            }

        # Verify if user predefined in table to allow user
        if not is_user_allowed(message.member_id):
            return {
                'statusCode': 401,
                'body': "Unauthorized: Member ID is not in Victorias Pre Defined Users Table"
            }

        return {
            'statusCode': 200,
            'body': "Authentication Successful"
        }