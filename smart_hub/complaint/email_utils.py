"""
Email utilities for Smart Hub complaint system
Using Django's built-in email backend with Gmail SMTP
"""
from django.core.mail import send_mail
from django.conf import settings
import logging
import os

# Set up logging
logger = logging.getLogger(__name__)

def send_admin_notification_new_complaint(complaint_data):
    """
    Send email notification to all admins when a new complaint is submitted
    
    Args:
        complaint_data (dict): Dictionary containing complaint information
            - complaint_id: Unique complaint ID
            - issue: Issue title/summary
            - description: Detailed description
            - area_name: Location/area of the complaint
            - category: Complaint category
            - citizen_name: Name of the citizen who submitted
            - citizen_email: Email of the citizen who submitted
            - date_time: Submission timestamp
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get admin emails from .env file
        admin_emails_str = os.getenv('ADMIN_EMAILS', '')
        if admin_emails_str:
            admin_emails = [email.strip() for email in admin_emails_str.split(',') if email.strip()]
        else:
            admin_emails = []
        
        if not admin_emails:
            logger.warning("No admin emails configured in .env file")
            print("⚠️ No admin emails configured. Please add ADMIN_EMAILS to .env file")
            return False
        
        subject = f"🚨 New Complaint #{complaint_data['complaint_id']}: {complaint_data['issue']}"
        
        message = f"""🚨 NEW COMPLAINT ALERT - Smart City Hub

A new complaint has been submitted and requires admin attention.

📋 COMPLAINT DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Complaint ID: #{complaint_data['complaint_id']}
• Issue Title: {complaint_data['issue']}
• Description: {complaint_data['description']}
• Location/Area: {complaint_data['area_name']}
• Category: {complaint_data['category']}
• Status: Open (Newly Submitted)
• Date & Time: {complaint_data['date_time']}

👤 CITIZEN INFORMATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Name: {complaint_data['citizen_name']}
• Email: {complaint_data['citizen_email']}

⚡ ACTION REQUIRED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Please log into the admin dashboard to review this complaint and take appropriate action.

You can contact the citizen directly at: {complaint_data['citizen_email']}

---
Smart City Hub - Automated Admin Notification
This email was sent from: {settings.EMAIL_HOST_USER}
"""
        
        # Send email to all admin emails
        for admin_email in admin_emails:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin_email],
                    fail_silently=False
                )
                print(f"✅ Admin notification sent to: {admin_email}")
                logger.info(f"📧 Admin notification sent to {admin_email} for complaint #{complaint_data['complaint_id']}")
            except Exception as e:
                print(f"❌ Failed to send to {admin_email}: {str(e)}")
                logger.error(f"Failed to send admin notification to {admin_email}: {str(e)}")
        
        print(f"📧 Admin notifications sent for complaint #{complaint_data['complaint_id']}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending admin notifications: {str(e)}")
        print(f"❌ Error sending admin notifications: {str(e)}")
        return False

def send_issue_status_change_mail(citizen_email, citizen_name, complaint_id, issue_title, old_status, new_status):
    """
    Send email notification to citizen when complaint status changes
    
    Args:
        citizen_email: Email address of the citizen
        citizen_name: Name of the citizen
        complaint_id: ID of the complaint
        issue_title: Title of the issue
        old_status: Previous status
        new_status: New status
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Determine the subject and message based on new status
        if new_status.lower() == 'resolved':
            subject = f"✅ Issue Cleared: {issue_title}"
            message = f"""Hello {citizen_name},

Great news! Your reported issue has been resolved.

📋 Complaint Details:
• Complaint ID: #{complaint_id}
• Issue: {issue_title}
• Status: {old_status} → {new_status}

Thank you for bringing this matter to our attention. We appreciate your patience and for using Smart City Hub.

If you have any questions or concerns about this resolution, please don't hesitate to contact us.

Best regards,
Smart City Hub Team
"""
        elif new_status.lower() == 'in-progress':
            subject = f"🔄 Issue Update: {issue_title}"
            message = f"""Hello {citizen_name},

We wanted to update you on your reported issue.

📋 Complaint Details:
• Complaint ID: #{complaint_id}
• Issue: {issue_title}
• Status: {old_status} → {new_status}

Our team is now actively working on resolving your complaint. We will keep you informed of any further updates.

Thank you for your patience.

Best regards,
Smart City Hub Team
"""
        elif new_status.lower() == 'closed':
            subject = f"📁 Issue Closed: {issue_title}"
            message = f"""Hello {citizen_name},

Your complaint has been closed.

📋 Complaint Details:
• Complaint ID: #{complaint_id}
• Issue: {issue_title}
• Status: {old_status} → {new_status}

If you believe this issue requires further attention, please feel free to submit a new complaint or contact our support team.

Thank you for using Smart City Hub.

Best regards,
Smart City Hub Team
"""
        else:
            # Generic status change message
            subject = f"📢 Status Update: {issue_title}"
            message = f"""Hello {citizen_name},

Your complaint status has been updated.

📋 Complaint Details:
• Complaint ID: #{complaint_id}
• Issue: {issue_title}
• Status: {old_status} → {new_status}

We will continue to keep you informed about any changes to your complaint.

Best regards,
Smart City Hub Team
"""

        # Send the email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[citizen_email],
            fail_silently=False
        )
        
        logger.info(f"📧 Status change email sent to {citizen_email} for complaint #{complaint_id}")
        print(f"✅ Email sent successfully to {citizen_name} ({citizen_email})")
        print(f"   Subject: {subject}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending status change email: {str(e)}")
        print(f"❌ Failed to send email to {citizen_email}: {str(e)}")
        return False

def send_issue_cleared_mail(citizen_email, issue_title):
    """
    Simplified function for backward compatibility
    """
    try:
        subject = f"Issue Cleared: {issue_title}"
        message = f"""Hello,

Your reported issue '{issue_title}' has been resolved.

Thank you for using Smart City Hub.

Regards,
Smart City Hub Team"""
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[citizen_email],
            fail_silently=False
        )
        
        logger.info(f"📧 Issue cleared email sent to {citizen_email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending issue cleared email: {str(e)}")
        return False