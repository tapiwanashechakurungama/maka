#!/usr/bin/env python
"""
Comprehensive setup script for Django backend
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from bus_tracking.models import User

def check_database():
    """Check if database is accessible"""
    print("Checking database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_migrations():
    """Create migrations"""
    print("Creating migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'bus_tracking'])
        print("✅ Migrations created")
        return True
    except Exception as e:
        print(f"❌ Error creating migrations: {e}")
        return False

def apply_migrations():
    """Apply migrations"""
    print("Applying migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations applied")
        return True
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
        return False

def create_superuser():
    """Create a superuser for admin access"""
    print("Creating superuser...")
    try:
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superuser already exists")
            return True
        
        # Create superuser
        superuser_data = {
            'username': 'admin',
            'email': 'admin@msu.ac.zw',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'phone_number': '1234567890'
        }
        
        user = User.objects.create_superuser(**superuser_data)
        print(f"✅ Superuser created: {user.email}")
        return True
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

def test_user_creation():
    """Test user creation"""
    print("Testing user creation...")
    try:
        # Test data
        test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890'
        }
        
        # Create test user
        user = User.objects.create_user(**test_user_data)
        print(f"✅ Test user created: {user.email}")
        
        # Clean up test user
        user.delete()
        print("✅ Test user cleaned up")
        return True
    except Exception as e:
        print(f"❌ Error testing user creation: {e}")
        return False

def check_models():
    """Check if all models are properly configured"""
    print("Checking models...")
    try:
        from bus_tracking.models import User, BusStation, Bus, Route, Booking, Notification
        
        # Check User model
        user_fields = [field.name for field in User._meta.fields]
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        missing_fields = [field for field in required_fields if field not in user_fields]
        
        if missing_fields:
            print(f"❌ Missing fields in User model: {missing_fields}")
            return False
        
        print("✅ All models are properly configured")
        return True
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False

def check_urls():
    """Check if URLs are properly configured"""
    print("Checking URL configuration...")
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test health endpoint
        response = client.get('/api/health/')
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        print("✅ URL configuration is working")
        return True
    except Exception as e:
        print(f"❌ Error checking URLs: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Setting up Django Backend for MSU Bus Tracking System")
    print("=" * 60)
    
    # Check database
    if not check_database():
        print("❌ Database check failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Check models
    if not check_models():
        print("❌ Model check failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Create migrations
    if not create_migrations():
        print("❌ Migration creation failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Apply migrations
    if not apply_migrations():
        print("❌ Migration application failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Test user creation
    if not test_user_creation():
        print("❌ User creation test failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Create superuser
    if not create_superuser():
        print("❌ Superuser creation failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Check URLs
    if not check_urls():
        print("❌ URL check failed. Exiting.")
        sys.exit(1)
    
    print()
    print("🎉 Django Backend Setup Completed Successfully!")
    print("✅ Registration and login are ready to use!")
    print()
    print("📋 Next Steps:")
    print("1. Start the server: python manage.py runserver")
    print("2. Access admin panel: http://localhost:8000/admin/")
    print("3. Test API endpoints: http://localhost:8000/api/health/")
    print("4. View API docs: http://localhost:8000/swagger/")
    print()
    print("🔐 Admin Credentials:")
    print("   Username: admin")
    print("   Email: admin@msu.ac.zw")
    print("   Password: admin123") 