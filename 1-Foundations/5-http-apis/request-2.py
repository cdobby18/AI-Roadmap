# POST = sending data

import requests

# Always use json= parameter, not data=
# json= automatically sets Content-Type: application/json
payload = {
    'name': 'Carl',
    'message': 'Hello from Python!'
}

response = requests.post(
    'https://httpbin.org/post',
    json=payload
)

print(response.status_code)   # 200
print(response.json()['json'])  # echoes back what you sent

# CALLING AN AI API

import requests
import os
from dotenv import load_dotenv

load_dotenv()  # load your .env file

response = requests.post(
    'https://api.anthropic.com/v1/messages',
    headers={
        'x-api-key': os.getenv('ANTHROPIC_API_KEY'),
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    },
    json={
        'model': 'claude-sonnet-4-20250514',
        'max_tokens': 1024,
        'messages': [{
            'role': 'user',
            'content': 'What is RAG?'
        }]
    }
)

data = response.json()
print(data['content'][0]['text'])  # the AI's response


# SENDING DATA

url =  ('https://api.anthropic.com/v1/messages')
response = requests.post(url, data={'field': 'value'})

# Uploading a file
with open('document.pdf', 'rb') as f:
    response = requests.post(url, files={'file': f})