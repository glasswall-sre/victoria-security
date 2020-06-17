import boto3
import base64
from botocore.exceptions import ClientError
from typing import Dict

def get_secret() -> Dict:
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