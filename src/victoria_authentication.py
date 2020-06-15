from src.azure_if import AzureIF
from src.slack_if import SlackIF
from src.aws_if import AwsIF

class VictoriaAuthentication:
    @staticmethod
    def authenticate(message, slack_email, secrets):
        # Verify Slack Token is Valid and existant in request
        if not SlackIF.is_valid_slack_verification_token(message.token, secrets):
            return {
                'statusCode': 401,
                'body': "Unauthorized: Invalid Token, Request suspected not coming from Slack"
            }

        # Verify User is in Glasswall Azure Active Directory
        if not AzureIF.is_user_in_ad_filtered( slack_email, secrets ):
            return {
                'statusCode': 401,
                'body': "Unauthorized: Slack User is not in Azure Active Directory"
            }

        # Verify User is from SRE Group Not-General function
        if not AzureIF.is_user_in_sre_ad_group( slack_email, secrets ):
            return {
                'statusCode': 401,
                'body': "Unauthorized: Slack User is not in Azure Active Directory Group (SRE Team)"
            }

        # Verify if user predefined in table to allow user
        if not AwsIF.is_user_allowed(message.member_id):
            return {
                'statusCode': 401,
                'body': "Unauthorized: Member ID is not in Victorias Pre Defined Users Table"
            }

        return {
            'statusCode': 200,
            'body': "Authentication Successful"
        }