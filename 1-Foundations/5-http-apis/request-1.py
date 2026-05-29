# GET REQUESTS = fetch data

import requests

# Make a GET request
response = requests.get('https://httpbin.org/get')

print(response.status_code)   # 200 = success
print(response.text)          # raw text response
print(response.json())        # parsed as Python dict
print(response.headers)       # response headers


# SENDING QUERY PARAMETERS  

# Pass params as a dictionary — cleaner and safer
params = {
    'name': 'carl',
    'course': 'ai engineering'
}

response = requests.get('https://httpbin.org/get', params=params)
print(response.url)   # shows the full URL that was built
print(response.json())


# PARSING JSON
# response.json() converts JSON to a Python dict automatically
data = response.json()

# Access specific fields
print(data['args'])         # query params you sent
print(data['origin'])       # your IP address



"""
STATUS CODES:

200 = OK — success
201 = Created — POST worked
400 = Bad request — your fault
401 = Unauthorized — bad API key
404 = Not found
500 = Server error — their fault

"""