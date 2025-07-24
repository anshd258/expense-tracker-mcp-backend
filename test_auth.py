"""
Test script to verify authentication setup
Run this after starting the server to test the authentication flow
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth_flow():
    print("Testing Authentication Flow...")
    
    # 1. Test unauthenticated access to protected endpoint
    print("\n1. Testing unauthenticated access to /api/v1/auth/me:")
    response = requests.get(f"{BASE_URL}/api/v1/auth/me")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # 2. Register a test user
    print("\n2. Registering a test user:")
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=register_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   User created: {response.json()}")
    else:
        print(f"   Response: {response.json()}")
    
    # 3. Login to get token
    print("\n3. Logging in to get token:")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/token", json=login_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        print(f"   Token received: {token[:20]}...")
    else:
        print(f"   Response: {response.json()}")
        return
    
    # 4. Test authenticated access
    print("\n4. Testing authenticated access to /api/v1/auth/me:")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   User info: {response.json()}")
    
    # 5. Test Swagger UI
    print("\n5. Check Swagger UI:")
    print(f"   Open {BASE_URL}/docs in your browser")
    print("   You should see:")
    print("   - An 'Authorize' button at the top right")
    print("   - A lock icon next to protected endpoints")
    print("   - Click 'Authorize' and enter the token to test endpoints")

if __name__ == "__main__":
    test_auth_flow()