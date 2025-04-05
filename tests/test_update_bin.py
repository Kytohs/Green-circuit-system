import requests

url = "http://127.0.0.1:5000/update-bin"
data = {
    "bin_id": "5678",
    "weight": 90,
    "location": "Main Street",
    "latitude": -1.3000,
    "longitude": 36.9000
}

response = requests.post(url, json=data)
print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())
