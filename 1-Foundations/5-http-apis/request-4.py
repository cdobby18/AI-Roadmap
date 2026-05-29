# ERROR HANDLING

import requests

url =  ('https://api.anthropic.com/v1/messages')

try:
    response = requests.get(url, timeout=10)

    # raise_for_status() raises an exception for 4xx and 5xx
    response.raise_for_status()

    data = response.json()
    print('Success:', data)

except requests.exceptions.Timeout:
    print('Request timed out — try again later')

except requests.exceptions.ConnectionError:
    print('No internet connection')

except requests.exceptions.HTTPError as e:
    print(f'HTTP error: {e.response.status_code}')
    if e.response.status_code == 401:
        print('Check your API key')
    elif e.response.status_code == 429:
        print('Rate limit hit — slow down')

except requests.exceptions.RequestException as e:
    print(f'Something went wrong: {e}')  # catch-all