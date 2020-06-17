from slack.errors import SlackApiError
from typing import Dict

def get_member_email(client, member_id : str):
    user_info = client.users_info(user=member_id)
    return user_info.data['user']['profile']['email'] if user_info.data['ok'] == True else None

def get_email(client, member_id : str):
    return get_member_email(client, member_id)

def is_valid_slack_verification_token(event_token : str, secrets : Dict) -> bool:
    return event_token == secrets["VERIFICATION_TOKEN"]

