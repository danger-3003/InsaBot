import requests

url = 'http://localhost:8000/like_post'

data = {
    'username': 'dummy_username',
    'password': 'dummy_password',
    'post_url': 'https://www.instagram.com/p/ABC123/'
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.json())
