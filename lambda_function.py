import json
import urllib2

VERIFY_TOKEN = "VERIFY_TOKEN"
ACCESS_TOKEN = "ACCESS_TOKEN"


def lambda_handler(event, context):
    if event['context']['http-method'] == "GET":
        if event['params']['querystring']['hub.verify_token'] == VERIFY_TOKEN:
            return int(event['params']['querystring']['hub.challenge'])
    elif event['context']['http-method'] == "POST":
        sender_id = event['body-json']['entry'][0]['messaging'][0]['sender']['id']
        message_text = event['body-json']['entry'][0]['messaging'][0]['message']['text']
        
        message_data = {
            "recipient": {"id": sender_id},
            "message": {"text": message_text}
            }

        request = urllib2.Request("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN)
        request.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(request, json.dumps(message_data))
