import requests
import json

# Test shipping label generation without shipping code
url = "http://localhost:8002/shipping-labels/generate"

# Test data dengan shipping_code kosong
test_data = {
    "sender_name": "Test Sender",
    "sender_phone": "081234567890",
    "recipient_name": "Test Recipient", 
    "recipient_address": "Jl. Test No. 123, Kota Test",
    "recipient_phone": "081987654321",
    "shipping_code": ""  # Empty shipping code
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer test-token"  # You'll need a valid token
}

try:
    response = requests.post(url, json=test_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Shipping label with empty code works!")
    else:
        print("❌ Shipping label generation failed")
        
except Exception as e:
    print(f"❌ Error: {e}")