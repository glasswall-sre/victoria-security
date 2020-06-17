import json

from slack import WebClient
from slackbot_authentication.authentication_rules import run_authentication_rules
import slackbot_authentication.slack_utils as slack_utils
from slackbot_authentication.secrets import get_secret
from slackbot_authentication.audit_log import AuditLog
from slackbot_authentication.slack_message_event import SlackMessageEvent
import shlex
import requests
from typing import Dict, List

def call_victoria(shlex : List, secrets : Dict) -> Dict:
    """Make a POST request to V.I.C.T.O.R.I.A

    Args:
        shlex: A shlex list of commands to pass into Victoria.
        secrets: The secrets read from secrets.get_secrets()

    Returns:
        { 
            statusCode: int, 
            body: str
        }
    """
    url = secrets["VICTORIA_URL"]
    data = {
        'args': shlex
    }
    r = requests.post(url, json=data)
    return {
        'statusCode' : r.status_code,
        'body': r.json()
    }

def request_validation(event, event_content : Dict, secrets : Dict) -> Dict:
    """Validate the request from API Gateway to Lambda in production.
    Function will ensure any retrys are responded to as soon as possible with 200
    otherwise 3 retrys happen and will run the lambda to completion 4 times.

    Args:
        event: event from API Gateway
        event_content: event body value
        secrets: The secrets read from secrets.get_secrets()

    Returns:
        { 
            statusCode: int, 
            body: str
        }
        statusCode 200 should be returned immediately to avoid more retrys.
        statusCode 100 should allow continuing of execution.
    """
    # Don't Accept Retrys
    if "X-Slack-Retry-Num" in event.get("headers"):
        return { 'statusCode': 200, 'body': "OK" }

    # Check Message Is Not From Bot
    if "bot_id" in event_content.get("event"):
        if secrets["BOT_ID"] == event_content.get("event").get("bot_id"):
            return { 'statusCode': 200, 'body': "OK" }
    
    return { 'statusCode': 100, 'body': "continue" }

def lambda_handler(event, context):
    event_content = json.loads(event.get("body"))
    secrets = json.loads(get_secret())

    # Required checks to ensure bot does not response to itself
    result = request_validation(event, event_content, secrets)
    if result['statusCode'] == 200:
        return result

    # Pass event into lightweight object to pass around
    try:
        message = SlackMessageEvent(event_content)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }

    slack_client = WebClient(token=secrets["BOT_USER_OAUTH_ACCESS_TOKEN"])
    slack_email = slack_utils.get_email(slack_client, message.member_id)

    # Authenticate, If fails returns message
    response = run_authentication_rules(message, slack_email, secrets)
    if response['statusCode'] != 200:
        slack_client.chat_postMessage(channel=message.channel, text=response['body'])
        return {
            'statusCode': 403,
            'body': "Access Unauthorised."
        }

    # Shlex Text
    text = event_content.get("event").get("text")
    shlex_text = shlex.split(text)
    shlex_text.pop(0)

    audit = AuditLog()

    # Add to Audit Log
    response = audit.insert_request_to_audit_log(message.member_id, text)
    if response['statusCode'] != 200:
        return {
            'statusCode': 502,
            'body': "Could Not Create Audit Record. Aborting Request to Victoria"
        }

    # Call Victoria
    response = call_victoria(shlex_text, secrets)
    if response['statusCode'] == 200:
        slack_client.chat_postMessage(channel=message.channel, text=response['body'])

        # Audit Response
        response = audit.insert_response_to_audit_log(message.member_id, response)
        if response['statusCode'] != 200:
            return {
                'statusCode' : 502,
                'body' : "Response Could not be audited."
            }
    else:
        slack_client.chat_postMessage(channel=message.channel, text="Request to Victoria API was unsuccessful. Try Again")

    # Reached End, All OK
    return {
        'statusCode': 200,
        'body': "OK"
    }