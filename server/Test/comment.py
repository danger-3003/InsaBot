import requests

url = 'http://localhost:8000/comment_on_post'  # Update with your actual server URL if different

# Replace 'dummy_username', 'dummy_password', 'post_url', and 'comment_text' with your actual dummy credentials and data
data = {
    'username': '',
    'password': '',
    'post_url': 'https://www.instagram.com/p/ABC123/',
    'comment_text': 'This is a test comment'
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.json())
