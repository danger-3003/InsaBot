import requests

url = 'http://localhost:8000/check_login'  # Update with your actual server URL if different

# Replace 'dummy_username' and 'dummy_password' with your actual dummy credentials
data = {'username': 'localhost_400', 'password': 'instagram'}

response = requests.post(url, data=data)

print(response.status_code)
print(response.json())
