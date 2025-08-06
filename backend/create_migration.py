#!/usr/bin/env python
"""
Script to create and apply migrations for User model changes
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
django.setup()

from django.core.management import execute_from_command_line

def create_migrations():
    """Create migrations for model changes"""
    print("Creating migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✅ Migrations created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating migrations: {e}")
        return False

def apply_migrations():
    """Apply migrations"""
    print("Applying migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations applied successfully")
        return True
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
        return False

if __name__ == '__main__':
    print("🔄 Setting up database migrations...")
    print("=" * 50)
    
    # Create migrations
    if not create_migrations():
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    print()
    
    # Apply migrations
    if not apply_migrations():
        print("❌ Failed to apply migrations")
        sys.exit(1)
    
    print()
    print("🎉 Database setup completed successfully!")
    print("✅ User model is ready for registration and login!") 