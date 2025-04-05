import requests

url = "http://127.0.0.1:5000/login"
data = {"username": "collector", "password": "password123"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)

print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())
