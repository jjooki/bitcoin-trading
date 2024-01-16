import requests
import os

# Send a message whatever I want to my slack channel
def alarm(text):
    token = os.getenv('SLACK_TOKEN')
    channel = "#trading-alarm"
    
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+ token},
        data={"channel": channel, "text": text}
    )
    print(response.status_code)