import json
import os
import requests

token = os.getenv("WHATSAPP_TOKEN")
base_url="https://graph.facebook.com/v19.0/206459855891807/messages"
def send_message(message, data):
    datax = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": data['to'],
        "context": {
            "message_id": data['wam_id'],
        },
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message,
        },
    })

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Cookie": "ps_l=0; ps_n=0",
    }

    response = requests.post(base_url, headers=headers, data=datax)
    
    if response.status_code == 200:
        return True
    else:
        print(response.text)
        return False