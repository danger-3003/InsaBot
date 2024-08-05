import requests

url = 'http://localhost:8000/keep_story'  # Update with your actual server URL if different

# Replace 'dummy_username' and 'dummy_password' with your actual dummy credentials
data = {
    'username': 'dummy_username',
    'password': 'dummy_password'
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.json())
