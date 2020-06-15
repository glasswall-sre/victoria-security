import json

from slack import WebClient
from src.victoria_authentication import VictoriaAuthentication
from src.slack_if import SlackIF
from src.victoria_if import VictoriaIF
from src.aws_if import AwsIF
from src.slack_message_event import SlackMessageEvent

def request_validation(event, event_content, secrets):
    #Don't Accept Retrys
    if "X-Slack-Retry-Num" in event.get("headers"):
        return { 'statusCode': 200, 'body': "OK" }

    #Check Message Is Not From Bot
    if "bot_id" in event_content.get("event"):
        if secrets["BOT_ID"] == event_content.get("event").get("bot_id"):
            return { 'statusCode': 200, 'body': "OK" }
    
    return None

def lambda_handler(event, context):
    event_content = json.loads( event.get("body") )
    secrets = json.loads( AwsIF.get_secret() )

    # Required checks to ensure bot does not response to itself
    result = request_validation(event, event_content, secrets)
    if result != None:
        return result

    # Pass event into leightweight bject to pass around
    try:
        message = SlackMessageEvent(event_content)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }

    slack_client = WebClient(token=secrets["BOT_USER_OAUTH_ACCESS_TOKEN"])
    slack_email = SlackIF.get_email(slack_client, message.member_id)

    # Authenticate, If fails returns message
    response = VictoriaAuthentication.authenticate(message, slack_email, secrets)
    if response['statusCode'] != 200:
        slack_client.chat_postMessage(channel=message.channel, text=response['body'])
        return {
            'statusCode': 403,
            'body': "Access Unauthorised."
        }

    # Shlex Text
    text = event_content.get("event").get("text")
    values = text.replace(secrets["BOT_MEMBER_ID"] + " ", "")
    shlex = values.split(" ")

    # Add to Audit Log
    response = AwsIF.insert_request_to_audit_log(message.member_id, text)
    if response['statusCode'] != 200:
        return {
            'statusCode': 502,
            'body': "Could Not Create Audit Record. Aborting Request to Victoria"
        }

    # Call Victoria
    response = VictoriaIF.call_victoria(shlex, secrets)
    if response['statusCode'] == 200:
        slack_client.chat_postMessage(channel=message.channel, text=response['body'])

        # Audit Response
        response = AwsIF.insert_response_to_audit_log(message.member_id, response)
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
    