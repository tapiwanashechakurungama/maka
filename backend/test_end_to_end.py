#!/usr/bin/env python
"""
End-to-end test script for registration and login
"""
import os
import sys
import django
import requests
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
django.setup()

BASE_URL = 'http://localhost:8000/api'

def test_registration():
    """Test user registration with mobile app format"""
    print("Testing user registration...")
    
    # Test data in mobile app format
    registration_data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=registration_data)
        print(f"Registration Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Registration successful")
            return True
        else:
            print("❌ Registration failed")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_login():
    """Test user login"""
    print("Testing user login...")
    
    # Test data
    login_data = {
        'email': 'john.doe@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
        print(f"Login Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            token = response.json().get('token')
            if token:
                print("✅ Login successful - Token received")
                return token
            else:
                print("❌ Login failed - No token received")
                return None
        else:
            print("❌ Login failed")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_authenticated_request(token):
    """Test authenticated request with token"""
    print("Testing authenticated request...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f'{BASE_URL}/bookings/user/', headers=headers)
        print(f"Authenticated Request Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Authenticated request successful")
            return True
        else:
            print("❌ Authenticated request failed")
            return False
    except Exception as e:
        print(f"❌ Authenticated request error: {e}")
        return False

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    
    try:
        response = requests.get(f'{BASE_URL}/health/')
        print(f"Health Check Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Health check successful")
            return True
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def cleanup_test_user():
    """Clean up test user from database"""
    print("Cleaning up test user...")
    try:
        from bus_tracking.models import User
        User.objects.filter(email='john.doe@example.com').delete()
        print("✅ Test user cleaned up")
    except Exception as e:
        print(f"❌ Cleanup error: {e}")

if __name__ == '__main__':
    print("🧪 End-to-End Testing for Registration and Login")
    print("=" * 60)
    
    # Clean up any existing test user
    cleanup_test_user()
    
    # Test health check first
    if not test_health_check():
        print("❌ Health check failed. Make sure Django server is running.")
        print("   Start server with: python manage.py runserver")
        sys.exit(1)
    
    print()
    
    # Test registration
    if not test_registration():
        print("❌ Registration failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Test login
    token = test_login()
    if not token:
        print("❌ Login failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Test authenticated request
    if not test_authenticated_request(token):
        print("❌ Authenticated request failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Clean up
    cleanup_test_user()
    
    print("🎉 All End-to-End Tests Passed!")
    print("✅ Registration and login are working correctly!")
    print()
    print("📱 Mobile app can now:")
    print("   - Register new users")
    print("   - Login with email/password")
    print("   - Make authenticated API calls")
    print()
    print("🚀 Ready for mobile app testing!") 