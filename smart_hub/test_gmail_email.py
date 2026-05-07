"""
Test script for Gmail SMTP email functionality
Run this after setting up your Gmail app password in settings.py
"""
import os
import sys
import django

# Add the project root to Python path
sys.path.append('c:/Users/donga/Desktop/hackathon_2/smart_hub')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hub.settings')
django.setup()

from complaint.email_utils import send_issue_status_change_mail, send_admin_notification_new_complaint

def test_admin_notification():
    """
    Test admin notification for new complaints
    """
    print("🧪 Testing Admin Notification for New Complaints")
    print("=" * 60)
    
    # Test data for new complaint
    complaint_data = {
        'complaint_id': 456,
        'issue': 'Test New Complaint - Pothole on Main Street',
        'description': 'There is a large pothole on Main Street that needs immediate attention. It is causing damage to vehicles and creating a safety hazard.',
        'area_name': 'Downtown Main Street',
        'category': 'Roads',
        'citizen_name': 'John Doe',
        'citizen_email': 'johndoe@example.com',
        'date_time': 'September 30, 2025 at 02:30 PM'
    }
    
    print(f"📋 Test Complaint Details:")
    print(f"   ID: #{complaint_data['complaint_id']}")
    print(f"   Issue: {complaint_data['issue']}")
    print(f"   Area: {complaint_data['area_name']}")
    print(f"   Category: {complaint_data['category']}")
    print(f"   Citizen: {complaint_data['citizen_name']} ({complaint_data['citizen_email']})")
    print()
    
    try:
        print("📧 Attempting to send admin notification emails...")
        
        success = send_admin_notification_new_complaint(complaint_data)
        
        if success:
            print("✅ Admin notification emails sent successfully!")
            print("   Check admin inboxes for the new complaint alert.")
        else:
            print("❌ Admin notification emails failed to send.")
            print("   Check your .env ADMIN_EMAILS configuration.")
            
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print()
        print("🔧 Troubleshooting Steps:")
        print("1. Make sure ADMIN_EMAILS is configured in .env file")
        print("2. Verify admin email addresses are correct")
        print("3. Check Gmail SMTP configuration in settings.py")

def test_status_change_notification():
    """
    Test the status change email functionality with sample data
    """
    print("🧪 Testing Status Change Email Functionality")
    print("=" * 60)
    
    # Test data
    test_citizen_email = "dsivaji9100@gmail.com"  # Replace with your test email
    test_citizen_name = "Test Citizen"
    test_complaint_id = 123
    test_issue_title = "Test Issue - Broken Street Light"
    test_old_status = "open"
    test_new_status = "resolved"
    
    print(f"📋 Test Details:")
    print(f"   Citizen: {test_citizen_name} ({test_citizen_email})")
    print(f"   Complaint ID: #{test_complaint_id}")
    print(f"   Issue: {test_issue_title}")
    print(f"   Status Change: {test_old_status} → {test_new_status}")
    print()
    
    try:
        print("📧 Attempting to send test email...")
        
        success = send_issue_status_change_mail(
            citizen_email=test_citizen_email,
            citizen_name=test_citizen_name,
            complaint_id=test_complaint_id,
            issue_title=test_issue_title,
            old_status=test_old_status,
            new_status=test_new_status
        )
        
        if success:
            print("✅ Status change email sent successfully!")
            print("   Check the recipient's inbox for the test email.")
        else:
            print("❌ Status change email failed to send.")
            print("   Check your Gmail app password configuration.")
            
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print()
        print("🔧 Troubleshooting Steps:")
        print("1. Make sure you've replaced 'your_app_password' in settings.py")
        print("2. Verify your Gmail app password is correct")
        print("3. Ensure 2-Factor Authentication is enabled on your Gmail account")
        print("4. Check that 'smartcityhub.demo@gmail.com' is accessible")

def test_all_email_functionality():
    """
    Test both admin notifications and status change emails
    """
    print("🚀 Smart Hub Email System - Comprehensive Test")
    print("=" * 70)
    print()
    
    # Test admin notifications first
    test_admin_notification()
    print()
    print("-" * 70)
    print()
    
    # Test status change notifications
    test_status_change_notification()
    print()
    print("=" * 70)
    print("🎯 Testing Complete! Check email inboxes for test messages.")

if __name__ == "__main__":
    test_all_email_functionality()