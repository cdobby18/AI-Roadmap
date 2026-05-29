# HEADERS AND AUTH

import requests, os
from dotenv import load_dotenv

load_dotenv()

url =  ('https://api.anthropic.com/v1/messages')

# Headers tell the server about your request
headers = {
    'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
    'Content-Type': 'application/json',
    'User-Agent': 'MyAIApp/1.0'
}

payload = {
    'name': 'Carl',
    'message': 'Hello from Python!'
}

response = requests.get(url, headers=headers)

# Or for every request using a Session
session = requests.Session()
session.headers.update(headers)

# Now every request from this session includes the headers
r1 = session.get('https://api.example.com/data')
r2 = session.post('https://api.example.com/predict', json=payload)

# SESSIONS FOR REUSING CONNECTIONS:
# A Session reuses the same connection and headers
# More efficient when making multiple requests to the same API

session = requests.Session()
session.headers['Authorization'] = f'Bearer {api_key}'
session.headers['Content-Type'] = 'application/json'

# All calls share the same headers — no repetition
history = session.get('/conversations')
reply = session.post('/messages', json={'text': 'hello'})

# Use Sessions when building a chatbot that makes
# multiple calls to the same AI API per session