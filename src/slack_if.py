from slack.errors import SlackApiError

class SlackIF:
    @staticmethod
    def get_members_of_channel(client, channel_id):
        x = client.groups_info(channel=channel_id)
        return x.data['group']['members']
    
    @staticmethod
    def get_member_email(client, member_id):
        x = client.users_info(user=member_id)
        return x.data['user']['profile']['email'] if x.data['ok'] == True else None

    @staticmethod 
    def get_email(client, member_id):
        return SlackIF.get_member_email(client, member_id)

    @staticmethod
    def is_valid_slack_verification_token(event_token, secrets):
        return True if event_token == secrets["VERIFICATION_TOKEN"] else False

