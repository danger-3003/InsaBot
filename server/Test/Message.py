import requests

url = 'http://localhost:8000/message_multiple_ids' 

data = {
    'username': 'dummy_username',
    'password': 'dummy_password',
    'ids': ['instagram_id_1', 'instagram_id_2', 'instagram_id_3'],  
    'message_text': 'Hello from the script! This is a test message.'
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.json())

