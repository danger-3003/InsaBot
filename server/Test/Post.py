import requests

url = 'http://localhost:8000/post_to_instagram' 

data = {
    'username': 'dummy_username',
    'password': 'dummy_password',
    'image_path': '/path/to/your/image.jpg',
    'caption': 'Sample caption',
    'first_comment': 'First comment'
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.json())
