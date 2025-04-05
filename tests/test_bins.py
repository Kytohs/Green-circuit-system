import requests

url = "http://127.0.0.1:5000/bins"

try:
    response = requests.get(url)
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)  # Print full response to debug issues
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to Flask. Is Flask running?")
