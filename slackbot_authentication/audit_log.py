import datetime
import boto3
from typing import Dict
AUDIT_DB = 'VictoriaAuditTrail'

class AuditLog:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(AUDIT_DB)

    def insert_request_to_audit_log(self, member_id : str, command : str) -> Dict:
        """Insert the Request made into the audit log

        Args:
            member_id: slack member id who made request
            command: the text from the slack message to be logged for auditing

        Returns:
            {
                statusCode: int,
                body: str
            }
            statusCode 200 when authentication is successful
            statusCode not 200 when and issue, see body for details.
        """
        response = self.table.put_item(
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

    def insert_response_to_audit_log(self, member_id : str, response : Dict) -> Dict:
        """Insert the Response from Victoria into the audit log

        Args:
            member_id: slack member id who made request
            response: the text from victoria

        Returns:
            {
                statusCode: int,
                body: str
            }
            statusCode 200 when authentication is successful
            statusCode not 200 when and issue, see body for details.
        """
        response = self.table.put_item(
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