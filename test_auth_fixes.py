#!/usr/bin/env python3
"""
Test script to verify authentication API contract fixes
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/auth"

def test_endpoints():
    """Test all authentication endpoints to ensure they exist and return expected responses"""

    print("Testing authentication API endpoints...")

    # Test GET profile endpoint (should return 401 without auth)
    try:
        response = requests.get(f"{BASE_URL}/profile")
        print(f"GET /profile: Status {response.status_code} (expected 401 - Unauthorized)")
    except Exception as e:
        print(f"GET /profile: Error - {e}")

    # Test POST signup endpoint
    try:
        signup_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = requests.post(f"{BASE_URL}/signup", json=signup_data)
        print(f"POST /signup: Status {response.status_code}")
        if response.status_code == 200:
            print(f"  Response: {response.json().keys()}")
    except Exception as e:
        print(f"POST /signup: Error - {e}")

    # Test POST signin endpoint
    try:
        signin_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/signin", json=signin_data)
        print(f"POST /signin: Status {response.status_code}")
        if response.status_code == 200:
            resp_data = response.json()
            print(f"  Response keys: {resp_data.keys()}")
            print(f"  Has user: {'user' in resp_data}")
            print(f"  Has token: {'token' in resp_data}")
    except Exception as e:
        print(f"POST /signin: Error - {e}")

    # Test PUT password/change endpoint
    try:
        password_change_data = {
            "currentPassword": "testpass123",
            "newPassword": "newtestpass123"
        }
        response = requests.put(f"{BASE_URL}/password/change", json=password_change_data)
        print(f"PUT /password/change: Status {response.status_code} (expected 401 - Unauthorized)")
    except Exception as e:
        print(f"PUT /password/change: Error - {e}")

    # Test POST password/recovery endpoint
    try:
        recovery_data = {
            "email": "test@example.com"
        }
        response = requests.post(f"{BASE_URL}/password/recovery", json=recovery_data)
        print(f"POST /password/recovery: Status {response.status_code}")
        if response.status_code == 200:
            print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"POST /password/recovery: Error - {e}")

    # Test POST password/reset endpoint
    try:
        reset_data = {
            "token": "fake-token",
            "newPassword": "newpassword123"
        }
        response = requests.post(f"{BASE_URL}/password/reset", json=reset_data)
        print(f"POST /password/reset: Status {response.status_code}")
        if response.status_code == 200:
            print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"POST /password/reset: Error - {e}")

    print("\nEndpoint testing completed!")

if __name__ == "__main__":
    test_endpoints()