import boto3
from boto3.dynamodb.conditions import Key

AUTHED_USERS_DB = 'VictoriaMemberAccepter'

def is_user_allowed(target_member_id : str) -> bool:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(AUTHED_USERS_DB)
    result = table.query(
        KeyConditionExpression=Key('member_id').eq(target_member_id)
    )
    return True if result['Count'] == 1 else False
