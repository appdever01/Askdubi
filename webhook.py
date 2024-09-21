import os
import json
import requests
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Access token for your app
token = os.getenv("WHATSAPP_TOKEN")

# Sets server port and logs message on success
@app.route('/webhook', methods=['POST'])
def webhook_post():
    body = request.json
    if body.get('object'):
        entry = body.get('entry', [])[0]
        changes = entry.get('changes', [])[0]
        value = changes.get('value', {})
        messages = value.get('messages', [])

        if messages:
            message = messages[0]
            wam_id = message.get('id')
            username = value.get('contacts', [])[0].get('profile', {}).get('name')
            btn_id = ''
            msg_body = ''
            msg_type = message.get('type')

            if msg_type == 'interactive':
                btn_id = message.get('interactive', {}).get('button_reply', {}).get('id')
            elif msg_type == 'text':
                msg_body = message.get('text', {}).get('body')

            phone_number_id = value.get('metadata', {}).get('phone_number_id')
            display_phone_number = value.get('metadata', {}).get('display_phone_number')
            from_number = message.get('from')
            print({
                    "id": phone_number_id,
                    "username": username,
                    "wam_id": wam_id,
                    "phone_number": display_phone_number,
                    "msg": msg_body,
                    "to": from_number,
                    "type": msg_type,
                    "btn_id": btn_id
                })
            return '', 200
    else:
        return '', 404

@app.route('/webhook', methods=['GET'])
def webhook_get():
    verify_token = os.getenv("VERIFY_TOKEN")

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == verify_token:
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            return '', 403

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 1337)), debug=True)