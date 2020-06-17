import boto3
import base64
from botocore.exceptions import ClientError
from typing import Dict

def get_secret() -> Dict:
    """Obtain the secrets in the AWS Secrets Manager

    Returns:
        {
            "CLIENT_ID": <val>,
            "CLIENT_SECRET": <val>,
            "SRE_TEAM_AD_GROUP_OBJECT_ID": <val>,
            "BOT_USER_OAUTH_ACCESS_TOKEN": <val>,
            "VERIFICATION_TOKEN": <val>,
            "BOT_ID": <val>,
            "BOT_MEMBER_ID": <val>,
            "SLACK_SIGNING_SECRET": <val>,
            "SLACK_CLIENT_SECRET": <val>,
            "MEMBER_TABLE_NAME": <val>,
            "VICTORIA_URL": <val>
        }
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="eu-west-2"
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId="victoria-security-secrets"
        )
    except ClientError as e:
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])