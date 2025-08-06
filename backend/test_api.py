#!/usr/bin/env python
"""
Simple test script for Django API endpoints
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_health():
    """Test health check endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/health/')
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_register():
    """Test user registration"""
    data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '1234567890'
    }
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=data)
        print(f"Register: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Registration failed: {e}")
        return False

def test_login():
    """Test user login"""
    data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=data)
        print(f"Login: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 200:
            return response.json().get('token')
        return None
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def test_booking(token):
    """Test booking creation"""
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'from': 'MSU Main Campus',
        'to': 'City Center',
        'date': '2024-01-15',
        'time': '09:00 AM',
        'numberOfPassengers': 2,
        'phoneNumber': '1234567890'
    }
    try:
        response = requests.post(f'{BASE_URL}/bookings/create/', json=data, headers=headers)
        print(f"Booking: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Booking failed: {e}")
        return False

if __name__ == '__main__':
    print("Testing Django API endpoints...")
    
    # Test health check
    if not test_health():
        print("❌ Health check failed")
        exit(1)
    print("✅ Health check passed")
    
    # Test registration
    if not test_register():
        print("❌ Registration failed")
        exit(1)
    print("✅ Registration passed")
    
    # Test login
    token = test_login()
    if not token:
        print("❌ Login failed")
        exit(1)
    print("✅ Login passed")
    
    # Test booking
    if not test_booking(token):
        print("❌ Booking failed")
        exit(1)
    print("✅ Booking passed")
    
    print("🎉 All tests passed!") 