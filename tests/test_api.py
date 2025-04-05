import requests

url = "http://127.0.0.1:5000/update-bin"
data = {
    "bin_id": "1234",
    "weight": 85,
    "location": "City Park",
    "latitude": -1.2921,
    "longitude": 36.8219
}

response = requests.post(url, json=data)
print(response.json())  # Print API response
import requests

# Test login API
url = "http://127.0.0.1:5000/login"
data = {
    "username": "collector",
    "password": "password123"
}
response = requests.post(url, json=data)
print("Login Response:", response.json())

# Test get bin status
url = "http://127.0.0.1:5000/get-bin/B001"
response = requests.get(url)
print("Bin Status:", response.json())

# Test update bin data
url = "http://127.0.0.1:5000/update-bin"
data = {
    "bin_id": "B001",
    "weight": 85,
    "location": "City Park",
    "latitude": -1.2921,
    "longitude": 36.8219
}
response = requests.post(url, json=data)
print("Update Bin Response:", response.json())
