import requests

url = "http://127.0.0.1:5000/update-bin"
data = {
    "bin_id": "1234",
    "weight": 85,
    "location": "City Park",
    "latitude": -1.2921,
    "longitude": 36.8219
}

try:
    response = requests.post(url, json=data)
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)  # Print full response to debug issues
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to Flask. Is Flask running?")


