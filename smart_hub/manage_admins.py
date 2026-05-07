#!/usr/bin/env python
"""
Admin Management Script for Smart Hub
This script allows developers to manage admin users (create, update, delete, list)
"""

import os
import sys
import django
from django.core.management.base import BaseCommand
import hashlib

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hub.settings')
django.setup()

from complaint.models import Admin

class AdminManager:
    def __init__(self):
        print("=== Smart Hub Admin Management System ===")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_admin(self, username, email, password):
        """Create a new admin user"""
        try:
            # Check if admin already exists
            if Admin.objects.filter(email=email).exists():
                print(f"❌ Admin with email '{email}' already exists!")
                return False
            
            hashed_password = self.hash_password(password)
            admin = Admin.objects.create(
                username=username,
                email=email,
                password=hashed_password,
                role='admin'
            )
            print(f"✅ Admin '{username}' created successfully with ID: {admin.uid}")
            return True
        except Exception as e:
            print(f"❌ Error creating admin: {str(e)}")
            return False
    
    def list_admins(self):
        """List all admin users"""
        admins = Admin.objects.all()
        if not admins:
            print("📋 No admins found in the database.")
            return
        
        print(f"📋 Found {admins.count()} admin(s):")
        print("-" * 60)
        print(f"{'ID':<5} {'Username':<20} {'Email':<30}")
        print("-" * 60)
        for admin in admins:
            print(f"{admin.uid:<5} {admin.username:<20} {admin.email:<30}")
        print("-" * 60)
    
    def update_admin(self, admin_id, username=None, email=None, password=None):
        """Update an existing admin user"""
        try:
            admin = Admin.objects.get(uid=admin_id)
            
            if username:
                admin.username = username
            if email:
                # Check if new email already exists
                if Admin.objects.filter(email=email).exclude(uid=admin_id).exists():
                    print(f"❌ Email '{email}' is already in use by another admin!")
                    return False
                admin.email = email
            if password:
                admin.password = self.hash_password(password)
            
            admin.save()
            print(f"✅ Admin with ID {admin_id} updated successfully!")
            return True
        except Admin.DoesNotExist:
            print(f"❌ Admin with ID {admin_id} not found!")
            return False
        except Exception as e:
            print(f"❌ Error updating admin: {str(e)}")
            return False
    
    def delete_admin(self, admin_id):
        """Delete an admin user"""
        try:
            admin = Admin.objects.get(uid=admin_id)
            username = admin.username
            admin.delete()
            print(f"✅ Admin '{username}' (ID: {admin_id}) deleted successfully!")
            return True
        except Admin.DoesNotExist:
            print(f"❌ Admin with ID {admin_id} not found!")
            return False
        except Exception as e:
            print(f"❌ Error deleting admin: {str(e)}")
            return False
    
    def get_admin_details(self, admin_id):
        """Get details of a specific admin"""
        try:
            admin = Admin.objects.get(uid=admin_id)
            print(f"📋 Admin Details:")
            print(f"   ID: {admin.uid}")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Role: {admin.role}")
            return True
        except Admin.DoesNotExist:
            print(f"❌ Admin with ID {admin_id} not found!")
            return False
    
    def run(self):
        """Main interactive menu"""
        while True:
            print("\n" + "="*50)
            print("1. Create new admin")
            print("2. List all admins")
            print("3. Update admin")
            print("4. Delete admin")
            print("5. View admin details")
            print("6. Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                print("\n--- Create New Admin ---")
                username = input("Enter username: ").strip()
                email = input("Enter email: ").strip()
                password = input("Enter password: ").strip()
                
                if username and email and password:
                    self.create_admin(username, email, password)
                else:
                    print("❌ All fields are required!")
            
            elif choice == '2':
                print("\n--- All Admins ---")
                self.list_admins()
            
            elif choice == '3':
                print("\n--- Update Admin ---")
                self.list_admins()
                try:
                    admin_id = int(input("Enter admin ID to update: ").strip())
                    username = input("Enter new username (leave empty to skip): ").strip() or None
                    email = input("Enter new email (leave empty to skip): ").strip() or None
                    password = input("Enter new password (leave empty to skip): ").strip() or None
                    
                    if username or email or password:
                        self.update_admin(admin_id, username, email, password)
                    else:
                        print("❌ No updates provided!")
                except ValueError:
                    print("❌ Invalid admin ID!")
            
            elif choice == '4':
                print("\n--- Delete Admin ---")
                self.list_admins()
                try:
                    admin_id = int(input("Enter admin ID to delete: ").strip())
                    confirm = input(f"Are you sure you want to delete admin with ID {admin_id}? (y/N): ").strip().lower()
                    if confirm == 'y':
                        self.delete_admin(admin_id)
                    else:
                        print("❌ Deletion cancelled!")
                except ValueError:
                    print("❌ Invalid admin ID!")
            
            elif choice == '5':
                print("\n--- View Admin Details ---")
                self.list_admins()
                try:
                    admin_id = int(input("Enter admin ID to view: ").strip())
                    self.get_admin_details(admin_id)
                except ValueError:
                    print("❌ Invalid admin ID!")
            
            elif choice == '6':
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice! Please select 1-6.")

if __name__ == "__main__":
    manager = AdminManager()
    manager.run()