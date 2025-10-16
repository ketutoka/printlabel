import requests
import json

# Test registration endpoint with phone field
url = "http://localhost:8002/register"

test_data = {
    "name": "Test User",
    "email": "test@example.com",
    "phone": "081234567890",
    "password": "password123"
}

try:
    response = requests.post(url, json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ Registration with phone field works!")
    else:
        print("❌ Registration failed")
        
except Exception as e:
    print(f"❌ Error: {e}")