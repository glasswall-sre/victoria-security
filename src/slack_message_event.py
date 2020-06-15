class SlackMessageEvent:
    def __init__(self, event):
        self.member_id = event.get("event").get("user")
        self.team_id = event.get("event").get("team")
        self.channel = event.get("event").get("channel")
        self.token = event.get("token")

        if self.member_id == None or self.team_id == None or self.channel == None or self.token == None:
            raise ValueError
