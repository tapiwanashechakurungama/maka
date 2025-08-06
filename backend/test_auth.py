#!/usr/bin/env python
"""
Test script for authentication (registration and login)
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
django.setup()

from bus_tracking.models import User
from bus_tracking.serializers import UserSerializer, LoginSerializer
from rest_framework.test import APITestCase
from django.test import TestCase

def test_user_creation():
    """Test user creation directly"""
    print("Testing user creation...")
    
    # Test data
    user_data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '1234567890'
    }
    
    try:
        # Create user using serializer
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"✅ User created successfully: {user.email}")
            return user
        else:
            print(f"❌ User creation failed: {serializer.errors}")
            return None
    except Exception as e:
        print(f"❌ User creation error: {e}")
        return None

def test_user_login():
    """Test user login"""
    print("Testing user login...")
    
    # Test data
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    try:
        # Test login using serializer
        serializer = LoginSerializer(data=login_data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            print(f"✅ Login successful: {user.email}")
            return user
        else:
            print(f"❌ Login failed: {serializer.errors}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_user_retrieval():
    """Test retrieving user from database"""
    print("Testing user retrieval...")
    
    try:
        user = User.objects.get(email='test@example.com')
        print(f"✅ User found: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   Name: {user.first_name} {user.last_name}")
        print(f"   Phone: {user.phone_number}")
        return user
    except User.DoesNotExist:
        print("❌ User not found in database")
        return None
    except Exception as e:
        print(f"❌ User retrieval error: {e}")
        return None

def cleanup_test_user():
    """Clean up test user"""
    print("Cleaning up test user...")
    try:
        User.objects.filter(email='test@example.com').delete()
        print("✅ Test user cleaned up")
    except Exception as e:
        print(f"❌ Cleanup error: {e}")

if __name__ == '__main__':
    print("🧪 Testing Django Authentication...")
    print("=" * 50)
    
    # Clean up any existing test user
    cleanup_test_user()
    
    # Test user creation
    user = test_user_creation()
    if not user:
        print("❌ User creation failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Test user retrieval
    retrieved_user = test_user_retrieval()
    if not retrieved_user:
        print("❌ User retrieval failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Test user login
    logged_in_user = test_user_login()
    if not logged_in_user:
        print("❌ User login failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Clean up
    cleanup_test_user()
    
    print("🎉 All authentication tests passed!")
    print("✅ Registration and login are working correctly!") 