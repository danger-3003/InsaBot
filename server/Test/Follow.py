import requests

url = 'http://localhost:8000/follow_user'  # Update with your actual server URL if different

# Replace 'dummy_username', 'dummy_password', and 'username_to_follow' with your actual dummy credentials and username
data = {
    'username': 'dummy_username',
    'password': 'dummy_password',
    'username_to_follow': 'username_to_follow'
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.json())
