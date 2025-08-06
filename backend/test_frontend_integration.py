#!/usr/bin/env python
"""
Comprehensive test script for frontend-backend integration
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

class FrontendBackendIntegrationTest:
    def __init__(self):
        self.token = None
        self.user = None
        self.test_booking_id = None
        self.test_notification_id = None
    
    def test_health_check(self):
        """Test health check endpoint"""
        print("🔍 Testing health check...")
        try:
            response = requests.get(f'{BASE_URL}/health/')
            if response.status_code == 200:
                print("✅ Health check passed")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_registration(self):
        """Test user registration"""
        print("🔍 Testing user registration...")
        registration_data = {
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        
        try:
            response = requests.post(f'{BASE_URL}/auth/register/', json=registration_data)
            if response.status_code == 201:
                print("✅ Registration successful")
                return True
            else:
                print(f"❌ Registration failed: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False
    
    def test_login(self):
        """Test user login"""
        print("🔍 Testing user login...")
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        
        try:
            response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.user = data.get('user')
                if self.token:
                    print("✅ Login successful - Token received")
                    return True
                else:
                    print("❌ Login failed - No token received")
                    return False
            else:
                print(f"❌ Login failed: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def test_create_booking(self):
        """Test booking creation"""
        print("🔍 Testing booking creation...")
        if not self.token:
            print("❌ No token available for booking test")
            return False
        
        booking_data = {
            'from': 'MSU Main Campus',
            'to': 'City Center',
            'date': '2024-01-15',
            'time': '09:00 AM',
            'numberOfPassengers': 2,
            'phoneNumber': '1234567890'
        }
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(f'{BASE_URL}/bookings/create/', json=booking_data, headers=headers)
            if response.status_code == 201:
                data = response.json()
                self.test_booking_id = data.get('booking_id')
                print("✅ Booking creation successful")
                return True
            else:
                print(f"❌ Booking creation failed: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Booking creation error: {e}")
            return False
    
    def test_get_user_bookings(self):
        """Test fetching user bookings"""
        print("🔍 Testing user bookings fetch...")
        if not self.token:
            print("❌ No token available for bookings test")
            return False
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(f'{BASE_URL}/bookings/user/', headers=headers)
            if response.status_code == 200:
                data = response.json()
                bookings = data.get('results', [])
                print(f"✅ User bookings fetched successfully - {len(bookings)} bookings")
                return True
            else:
                print(f"❌ User bookings fetch failed: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print(f"❌ User bookings fetch error: {e}")
            return False
    
    def test_cancel_booking(self):
        """Test booking cancellation"""
        print("🔍 Testing booking cancellation...")
        if not self.token or not self.test_booking_id:
            print("❌ No token or booking ID available for cancellation test")
            return False
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.put(f'{BASE_URL}/bookings/{self.test_booking_id}/cancel/', headers=headers)
            if response.status_code == 200:
                print("✅ Booking cancellation successful")
                return True
            else:
                print(f"❌ Booking cancellation failed: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Booking cancellation error: {e}")
            return False
    
    def test_get_notifications(self):
        """Test fetching notifications"""
        print("🔍 Testing notifications fetch...")
        if not self.token:
            print("❌ No token available for notifications test")
            return False
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(f'{BASE_URL}/notifications/', headers=headers)
            if response.status_code == 200:
                data = response.json()
                notifications = data.get('results', [])
                if notifications:
                    self.test_notification_id = notifications[0].get('id')
                print(f"✅ Notifications fetched successfully - {len(notifications)} notifications")
                return True
            else:
                print(f"❌ Notifications fetch failed: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Notifications fetch error: {e}")
            return False
    
    def test_mark_notification_read(self):
        """Test marking notification as read"""
        print("🔍 Testing mark notification as read...")
        if not self.token or not self.test_notification_id:
            print("❌ No token or notification ID available for mark read test")
            return False
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.put(f'{BASE_URL}/notifications/{self.test_notification_id}/read/', headers=headers)
            if response.status_code == 200:
                print("✅ Mark notification as read successful")
                return True
            else:
                print(f"❌ Mark notification as read failed: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Mark notification as read error: {e}")
            return False
    
    def test_mark_all_notifications_read(self):
        """Test marking all notifications as read"""
        print("🔍 Testing mark all notifications as read...")
        if not self.token:
            print("❌ No token available for mark all read test")
            return False
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.put(f'{BASE_URL}/notifications/mark-all-read/', headers=headers)
            if response.status_code == 200:
                print("✅ Mark all notifications as read successful")
                return True
            else:
                print(f"❌ Mark all notifications as read failed: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Mark all notifications as read error: {e}")
            return False
    
    def test_get_unread_count(self):
        """Test getting unread notification count"""
        print("🔍 Testing unread notification count...")
        if not self.token:
            print("❌ No token available for unread count test")
            return False
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(f'{BASE_URL}/notifications/unread-count/', headers=headers)
            if response.status_code == 200:
                data = response.json()
                unread_count = data.get('unreadCount', 0)
                print(f"✅ Unread count fetched successfully - {unread_count} unread")
                return True
            else:
                print(f"❌ Unread count fetch failed: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Unread count fetch error: {e}")
            return False
    
    def test_delete_notification(self):
        """Test deleting notification"""
        print("🔍 Testing notification deletion...")
        if not self.token or not self.test_notification_id:
            print("❌ No token or notification ID available for deletion test")
            return False
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.delete(f'{BASE_URL}/notifications/{self.test_notification_id}/', headers=headers)
            if response.status_code == 200:
                print("✅ Notification deletion successful")
                return True
            else:
                print(f"❌ Notification deletion failed: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Notification deletion error: {e}")
            return False
    
    def cleanup_test_data(self):
        """Clean up test data"""
        print("🧹 Cleaning up test data...")
        try:
            from bus_tracking.models import User, Booking, Notification
            User.objects.filter(email='testuser@example.com').delete()
            print("✅ Test data cleaned up")
        except Exception as e:
            print(f"❌ Cleanup error: {e}")
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🧪 Frontend-Backend Integration Testing")
        print("=" * 60)
        
        # Clean up any existing test data
        self.cleanup_test_data()
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Registration", self.test_registration),
            ("Login", self.test_login),
            ("Create Booking", self.test_create_booking),
            ("Get User Bookings", self.test_get_user_bookings),
            ("Get Notifications", self.test_get_notifications),
            ("Get Unread Count", self.test_get_unread_count),
            ("Mark Notification Read", self.test_mark_notification_read),
            ("Mark All Notifications Read", self.test_mark_all_notifications_read),
            ("Cancel Booking", self.test_cancel_booking),
            ("Delete Notification", self.test_delete_notification),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            print("-" * 40)
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        
        print(f"\n📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All integration tests passed!")
            print("✅ Frontend and backend are fully integrated!")
        else:
            print("❌ Some tests failed. Check the logs above.")
        
        # Clean up
        self.cleanup_test_data()
        
        return passed == total

if __name__ == '__main__':
    tester = FrontendBackendIntegrationTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1) 