import datetime
import boto3
from typing import Dict
AUDIT_DB = 'VictoriaAuditTrail'

class AuditLog:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(AUDIT_DB)

    def insert_request_to_audit_log(self, member_id : str, command : str) -> Dict:
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