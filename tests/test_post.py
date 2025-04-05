import requests

url = "http://127.0.0.1:5000/update-bin"
data = {
    "bin_id": "B002",
    "weight": 60,
    "location": "City Park",
    "latitude": -1.2921,
    "longitude": 36.8219
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print(response.json())  # Prints server response
