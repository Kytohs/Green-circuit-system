import requests

BASE_URL = "http://127.0.0.1:5000"

def test_register_collector():
    data = {
        "name": "Test User",
        "whatsapp": "+254758293126"
    }
    response = requests.post(f"{BASE_URL}/api/register-collector", json=data)
    assert response.status_code == 200

def test_get_bins():
    response = requests.get(f"{BASE_URL}/get-bins")
    assert response.status_code == 200
