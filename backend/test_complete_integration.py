#!/usr/bin/env python
"""
Complete Frontend-Backend Integration Test
"""
import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
django.setup()

BASE_URL = 'http://localhost:8000/api'

def test_complete_user_journey():
    """Test complete user journey from registration to booking"""
    print("🧪 Testing Complete User Journey")
    print("=" * 50)
    
    # Step 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f'{BASE_URL}/health/')
        if response.status_code != 200:
            print("❌ Health check failed")
            return False
        print("✅ Health check passed")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Step 2: User Registration
    print("\n2️⃣ Testing User Registration...")
    registration_data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=registration_data)
        if response.status_code != 201:
            print(f"❌ Registration failed: {response.status_code}")
            return False
        print("✅ Registration successful")
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    # Step 3: User Login
    print("\n3️⃣ Testing User Login...")
    login_data = {
        'email': 'john.doe@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code}")
            return False
        
        data = response.json()
        token = data.get('token')
        if not token:
            print("❌ No token received")
            return False
        print("✅ Login successful - Token received")
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 4: Create Booking
    print("\n4️⃣ Testing Booking Creation...")
    booking_data = {
        'from': 'MSU Main Campus',
        'to': 'City Center',
        'date': '2024-01-15',
        'time': '09:00 AM',
        'numberOfPassengers': 2,
        'phoneNumber': '1234567890'
    }
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/bookings/create/', json=booking_data, headers=headers)
        if response.status_code != 201:
            print(f"❌ Booking creation failed: {response.status_code}")
            return False
        
        booking_response = response.json()
        booking_id = booking_response.get('booking_id')
        if not booking_id:
            print("❌ No booking ID received")
            return False
        print("✅ Booking creation successful")
    except Exception as e:
        print(f"❌ Booking creation error: {e}")
        return False
    
    # Step 5: Get User Bookings
    print("\n5️⃣ Testing Get User Bookings...")
    try:
        response = requests.get(f'{BASE_URL}/bookings/user/', headers=headers)
        if response.status_code != 200:
            print(f"❌ Get bookings failed: {response.status_code}")
            return False
        
        bookings_data = response.json()
        bookings = bookings_data.get('results', [])
        if not bookings:
            print("❌ No bookings found")
            return False
        print(f"✅ User bookings fetched - {len(bookings)} bookings")
    except Exception as e:
        print(f"❌ Get bookings error: {e}")
        return False
    
    # Step 6: Get Notifications
    print("\n6️⃣ Testing Get Notifications...")
    try:
        response = requests.get(f'{BASE_URL}/notifications/', headers=headers)
        if response.status_code != 200:
            print(f"❌ Get notifications failed: {response.status_code}")
            return False
        
        notifications_data = response.json()
        notifications = notifications_data.get('results', [])
        notification_id = None
        if notifications:
            notification_id = notifications[0].get('id')
        print(f"✅ Notifications fetched - {len(notifications)} notifications")
    except Exception as e:
        print(f"❌ Get notifications error: {e}")
        return False
    
    # Step 7: Get Unread Count
    print("\n7️⃣ Testing Get Unread Count...")
    try:
        response = requests.get(f'{BASE_URL}/notifications/unread-count/', headers=headers)
        if response.status_code != 200:
            print(f"❌ Get unread count failed: {response.status_code}")
            return False
        
        unread_data = response.json()
        unread_count = unread_data.get('unreadCount', 0)
        print(f"✅ Unread count fetched - {unread_count} unread")
    except Exception as e:
        print(f"❌ Get unread count error: {e}")
        return False
    
    # Step 8: Mark Notification as Read (if exists)
    if notification_id:
        print("\n8️⃣ Testing Mark Notification as Read...")
        try:
            response = requests.put(f'{BASE_URL}/notifications/{notification_id}/read/', headers=headers)
            if response.status_code != 200:
                print(f"❌ Mark notification as read failed: {response.status_code}")
                return False
            print("✅ Mark notification as read successful")
        except Exception as e:
            print(f"❌ Mark notification as read error: {e}")
            return False
    
    # Step 9: Mark All Notifications as Read
    print("\n9️⃣ Testing Mark All Notifications as Read...")
    try:
        response = requests.put(f'{BASE_URL}/notifications/mark-all-read/', headers=headers)
        if response.status_code != 200:
            print(f"❌ Mark all notifications as read failed: {response.status_code}")
            return False
        print("✅ Mark all notifications as read successful")
    except Exception as e:
        print(f"❌ Mark all notifications as read error: {e}")
        return False
    
    # Step 10: Cancel Booking
    print("\n🔟 Testing Cancel Booking...")
    try:
        response = requests.put(f'{BASE_URL}/bookings/{booking_id}/cancel/', headers=headers)
        if response.status_code != 200:
            print(f"❌ Cancel booking failed: {response.status_code}")
            return False
        print("✅ Cancel booking successful")
    except Exception as e:
        print(f"❌ Cancel booking error: {e}")
        return False
    
    # Step 11: Delete Notification (if exists)
    if notification_id:
        print("\n1️⃣1️⃣ Testing Delete Notification...")
        try:
            response = requests.delete(f'{BASE_URL}/notifications/{notification_id}/', headers=headers)
            if response.status_code != 200:
                print(f"❌ Delete notification failed: {response.status_code}")
                return False
            print("✅ Delete notification successful")
        except Exception as e:
            print(f"❌ Delete notification error: {e}")
            return False
    
    print("\n🎉 Complete User Journey Test Passed!")
    return True

def test_mobile_app_data_formats():
    """Test that backend handles mobile app data formats correctly"""
    print("\n📱 Testing Mobile App Data Formats")
    print("=" * 50)
    
    # Test registration with mobile app format
    print("\n1️⃣ Testing Registration Format...")
    registration_data = {
        'firstName': 'Jane',
        'lastName': 'Smith',
        'email': 'jane.smith@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=registration_data)
        if response.status_code != 201:
            print(f"❌ Registration format test failed: {response.status_code}")
            return False
        print("✅ Registration format test passed")
    except Exception as e:
        print(f"❌ Registration format test error: {e}")
        return False
    
    # Test login with mobile app format
    print("\n2️⃣ Testing Login Format...")
    login_data = {
        'email': 'jane.smith@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
        if response.status_code != 200:
            print(f"❌ Login format test failed: {response.status_code}")
            return False
        
        data = response.json()
        if not data.get('token'):
            print("❌ Login format test failed - no token")
            return False
        print("✅ Login format test passed")
    except Exception as e:
        print(f"❌ Login format test error: {e}")
        return False
    
    # Test booking with mobile app format
    print("\n3️⃣ Testing Booking Format...")
    booking_data = {
        'from': 'MSU Campus',
        'to': 'Downtown',
        'date': '2024-01-20',
        'time': '10:30 AM',
        'numberOfPassengers': 1,
        'phoneNumber': '9876543210'
    }
    
    headers = {
        'Authorization': f'Bearer {data.get("token")}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/bookings/create/', json=booking_data, headers=headers)
        if response.status_code != 201:
            print(f"❌ Booking format test failed: {response.status_code}")
            return False
        print("✅ Booking format test passed")
    except Exception as e:
        print(f"❌ Booking format test error: {e}")
        return False
    
    print("\n🎉 Mobile App Data Format Tests Passed!")
    return True

def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    try:
        from bus_tracking.models import User
        User.objects.filter(email__in=['john.doe@example.com', 'jane.smith@example.com']).delete()
        print("✅ Test data cleaned up")
    except Exception as e:
        print(f"❌ Cleanup error: {e}")

def main():
    """Run all integration tests"""
    print("🚀 Complete Frontend-Backend Integration Testing")
    print("=" * 60)
    
    # Clean up any existing test data
    cleanup_test_data()
    
    # Test complete user journey
    journey_success = test_complete_user_journey()
    
    # Test mobile app data formats
    format_success = test_mobile_app_data_formats()
    
    # Clean up
    cleanup_test_data()
    
    print("\n📊 Final Results:")
    print(f"User Journey Test: {'✅ PASSED' if journey_success else '❌ FAILED'}")
    print(f"Data Format Test: {'✅ PASSED' if format_success else '❌ FAILED'}")
    
    if journey_success and format_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Frontend and backend are fully integrated!")
        print("✅ Mobile app can communicate with Django backend!")
        print("✅ All API endpoints are working correctly!")
        print("✅ Data formats are compatible!")
        return True
    else:
        print("\n❌ Some tests failed. Check the logs above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 