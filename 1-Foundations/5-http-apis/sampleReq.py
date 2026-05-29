import requests, os
from dotenv import load_dotenv

load_dotenv()

class AIClient:
    """A simple client for calling an AI API using requests."""

    BASE_URL = 'https://api.anthropic.com/v1'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': os.getenv('ANTHROPIC_API_KEY'),
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        })

    def chat(self, message: str, max_tokens: int = 500) -> str:
        """Send a message and get a response."""
        try:
            response = self.session.post(
                f'{self.BASE_URL}/messages',
                json={
                    'model': 'claude-sonnet-4-20250514',
                    'max_tokens': max_tokens,
                    'messages': [{'role': 'user', 'content': message}]
                },
                timeout=(5, 30)
            )
            response.raise_for_status()
            return response.json()['content'][0]['text']

        except requests.exceptions.Timeout:
            return 'Error: request timed out'
        except requests.exceptions.HTTPError as e:
            return f'Error {e.response.status_code}: check your API key'
        except requests.exceptions.RequestException as e:
            return f'Error: {e}'

# Usage
client = AIClient()
reply = client.chat('Explain RAG in one sentence')
print(reply)