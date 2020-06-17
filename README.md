<div align="center" style="text-align:center">
  
# victoria-security
A Slack interface and security layer into Victoria

</div>

# Motivation
To combine the technologies of:
- Slack (ChatOps)
- Azure AD Authentication
- [V.I.C.T.O.R.I.A](https://github.com/glasswall-sre/victoria)

# Pipeline Status
![CI](https://github.com/glasswall-sre/victoria-security/workflows/CI/badge.svg)
![CD](https://github.com/glasswall-sre/victoria-security/workflows/CD/badge.svg)
![](https://img.shields.io/badge/Glasswall%20SRE-Approved-success)

# Tech Framework
- Python
  - Slack API
  - Azure API
  - AWS SDK
- Serverless
  - Lambda
  - DynamoDB
- Github Actions

# Permissions
Prerequisites:
- Azure App Registration
  - Read All Users
  - Read All Groups
- Slack Bot Token Scopes
  - users:read:email
  - chat:write
  - app_mentions:read
  - im:read
  - im:write

# Local Development
Create a mock local debug file which will call the `lambda_function.lambda_handler(event, context)`
```
#local_debug.py
import lambda_function
event = {
    "headers" : {},
    "body" : """{
        "token":<token>,
        "event" : {
            "user" : <member_id>,
            "team" : <team_id>,
            "channel" : <channel_id>,
            "text":"<bot_id> -h"
        }
    }"""
}
context = None
lambda_function.lambda_handler(event, None)
```
`python local_debug.py`

# Test
`python -m pytest`

# Deployment
`serverless deploy --stage dev`

# Contributions
Contributions, ideas and bug reports are welcome and greatly appreciated. Please add issues for suggestions and bug reports or create a pull request.
