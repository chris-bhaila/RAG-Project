from typing import List

import requests
import json

backend_url = 'https://127.0.0.1:8000'
chatendpoint = "/chat"

def call_chatbot(messages, url=f"{backend_url}{chatendpoint}"):
    payload = {"question": messages}
    response = requests.post(url, json=payload)
    return json.loads(response.text)
