import requests

url = "http://127.0.0.1:8000/contact/"
data = {
    "name": "test1",
    "contact": "test@example.com",
    "message": "Testing API endpoint."
}

response = requests.post(url, json=data)
print(response.json())
