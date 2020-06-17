import boto3
from boto3.dynamodb.conditions import Key

AUTHED_USERS_DB = 'VictoriaMemberAccepter'

def is_user_allowed(target_member_id : str) -> bool:
    """Validate if user is within AWS DynamoDB table VictoriaMemberAccepter

    Args:
        target_member_id: Slack Member ID

    Returns:
        True if member_id is listed in the VictoriaMemberAccepter table
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(AUTHED_USERS_DB)
    result = table.query(
        KeyConditionExpression=Key('member_id').eq(target_member_id)
    )
    return result['Count'] == 1
