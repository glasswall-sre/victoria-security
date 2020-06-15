import datetime
import boto3
import base64
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

AUDIT_DB = 'VictoriaAuditTrail'
AUTHED_USERS_DB = 'VictoriaMemberAccepter'

class AwsIF:
    @staticmethod
    def insert_request_to_audit_log(member_id, command):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(AUDIT_DB)
        response = table.put_item(
            Item={
                'member_id' : member_id,
                'timestamp' : f'{datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}',
                'command' : command
            }
        )
        return {
            "statusCode" : response['ResponseMetadata']['HTTPStatusCode'],
            "body": ""
        }

    @staticmethod
    def insert_response_to_audit_log(member_id, response):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(AUDIT_DB)
        response = table.put_item(
            Item={
                'member_id' : member_id,
                'timestamp' : f'{datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}',
                'response_code' : response['statusCode'],
                'response_text' : response['body']
            }
        )
        return {
            "statusCode" : response['ResponseMetadata']['HTTPStatusCode'],
            "body": ""
        }

    @staticmethod
    def is_user_allowed(target_member_id):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(AUTHED_USERS_DB)
        result = table.query(
            KeyConditionExpression=Key('member_id').eq(target_member_id)
        )
        return True if result['Count'] == 1 else False

    @staticmethod
    def get_secret():
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