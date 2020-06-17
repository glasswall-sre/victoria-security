from slack.errors import SlackApiError
from typing import Dict

def get_email(client, member_id : str):
    """Obtain slack user email via the member id.
    Ensure Slack Bot has `users:read:email` enabled

    Args:
        client: Slack Client
        member_id: slack member id value

    Returns:
        member email (str | None)
    """
    user_info = client.users_info(user=member_id)
    return user_info.data['user']['profile']['email'] if user_info.data['ok'] == True else None

def is_valid_slack_verification_token(event_token : str, secrets : Dict) -> bool:
    """Verify the secret VERIFICATION_TOKEN against the event_token

    Args:
        event_token: Slack Client
        secrets: The secrets read from secrets.get_secrets()

    Returns:
        True if valid match. 
        False if match was not successful.
    """
    return event_token == secrets["VERIFICATION_TOKEN"]

