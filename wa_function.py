import json
import os
import requests

token = os.getenv("WHATSAPP_TOKEN")
base_url="https://graph.facebook.com/v19.0/422255167636678/messages"
def send_message(to, message):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(base_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        pass
    else:
        print("Failed to send message. Error:", response.text)

def send_image(to, image_url,caption):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": {"link": image_url, "caption": caption}
    }
    response = requests.post(base_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        pass
    else:
        print("Failed to send message. Error:", response.text)


def send_btn_msg(to, message, btn_list):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    refined_btn_list = []
    for btn in btn_list:
        refined_btn_list.append({"type": "reply", "reply": {'id': btn['id'], 'title': btn['title']}})
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": message
            },
            "action": {
                "buttons": refined_btn_list
            }
        }
    }
    response = requests.post(base_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        pass
    else:
        print("Failed to send message. Error:", response.text)
        
