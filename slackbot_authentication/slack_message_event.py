from typing import Dict

class SlackMessageEvent:
    def __init__(self, event : Dict):
        self.member_id = event["event"]["user"]
        self.team_id = event["event"]["team"]
        self.channel = event["event"]["channel"]
        self.token = event["token"]
