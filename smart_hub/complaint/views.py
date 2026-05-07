from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now, localtime
from django.conf import settings
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import jwt
import hashlib
import json

from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Complaint, Citizen, Admin
from .serializers import CitizenSerializer, AdminSerializer, ComplaintSerializer
from .utils import create_jwt, decode_jwt
from .email_utils import send_issue_status_change_mail, send_admin_notification_new_complaint

# Configure logging
logger = logging.getLogger(__name__)

SECRET_KEY = 'smart_city_hub'


# INDEX PAGE
def index(request):
    return render(request, 'login.html')

# Helper function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# SIGNUP VIEW (Only for Citizens)
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            return render(request, 'login.html', {'error': 'Username, email and password are required.'})

        hashed_password = hash_password(password)

        try:
            citizen = Citizen.objects.create(
                username=username,
                email=email,
                password=hashed_password,
                role='citizen'
            )
            return render(request, 'login.html', {'success': 'Account created successfully! Please login.'})
        except Exception:
            return render(request, 'login.html', {'error': 'Email already exists or registration failed.'})

    return render(request, 'login.html')

# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'citizen')
        
        hashed_password = hash_password(password)

        try:
            if role == 'citizen':
                user = Citizen.objects.get(email=email)
            else:  # role == 'admin'
                user = Admin.objects.get(email=email)
            
            if user.password == hashed_password:
                # Generate JWT token (expires in 5 hours)
                payload = {
                    'user_id': user.pk,
                    'role': user.role,
                    'exp': datetime.utcnow() + timedelta(hours=5)
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

                response = redirect('citizen_dashboard' if role == 'citizen' else 'admin_dashboard')
                response.set_cookie('jwt_token', token, max_age=5*60*60, httponly=True, samesite='Lax')
                return response
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials or role'})
        except (Citizen.DoesNotExist, Admin.DoesNotExist):
            return render(request, 'login.html', {'error': 'Invalid credentials or role'})

    return render(request, 'login.html')

# Helper function to decode JWT from cookie
def get_jwt_user(request):
    token = request.COOKIES.get('jwt_token')
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        role = payload['role']
        if role == 'citizen':
            user = Citizen.objects.get(pk=payload['user_id'])
        else:  # role == 'admin'
            user = Admin.objects.get(pk=payload['user_id'])
        return user, role
    except (jwt.ExpiredSignatureError, jwt.DecodeError, Citizen.DoesNotExist, Admin.DoesNotExist):
        return None

# CITIZEN DASHBOARD
def citizen_dashboard(request):
    jwt_user = get_jwt_user(request)
    if not jwt_user or jwt_user[1] != 'citizen':
        return redirect('login')
    user = jwt_user[0]

    # Handle new complaint submission
    if request.method == 'POST':
        issue = request.POST.get('issue')
        description = request.POST.get('description')
        area_name = request.POST.get('area_name')
        category = request.POST.get('category')
        if issue and description and area_name and category:
            # Create complaint with explicit timestamp
            complaint = Complaint(
                issue=issue,
                description=description,
                area_name=area_name,
                category=category,
                user_id=user
            )
            # The auto_now_add=True will automatically use the current time in the correct timezone
            complaint.save()
            
            # Send notification email to all admins about the new complaint
            try:
                complaint_data = {
                    'complaint_id': complaint.complaint_id,
                    'issue': complaint.issue,
                    'description': complaint.description,
                    'area_name': complaint.area_name,
                    'category': complaint.category,
                    'citizen_name': user.username,
                    'citizen_email': user.email,
                    'date_time': complaint.date_time.strftime('%B %d, %Y at %I:%M %p')
                }
                
                email_sent = send_admin_notification_new_complaint(complaint_data)
                
                if email_sent:
                    logger.info(f"📧 Admin notifications sent for new complaint #{complaint.complaint_id}")
                    print(f"✅ Admin notifications sent for complaint #{complaint.complaint_id}: {complaint.issue}")
                else:
                    logger.warning(f"⚠️ Failed to send admin notifications for complaint #{complaint.complaint_id}")
                    print(f"⚠️ Failed to send admin notifications for complaint #{complaint.complaint_id}")
                    
            except Exception as e:
                logger.error(f"❌ Error sending admin notifications for complaint #{complaint.complaint_id}: {str(e)}")
                print(f"❌ Error sending admin notifications: {str(e)}")

    complaints = Complaint.objects.filter(user_id=user)
    context = {
        'complaints': complaints,
        'user': user,
        'username': user.username,
        'email': user.email
    }
    return render(request, 'citizen.html', context)

# DELETE COMPLAINT (Citizens only)
def delete_complaint(request, complaint_id):
    jwt_user = get_jwt_user(request)
    if not jwt_user or jwt_user[1] != 'citizen':
        return redirect('login')
    
    user = jwt_user[0]
    
    try:
        # Get the complaint and verify it belongs to the current user
        complaint = Complaint.objects.get(pk=complaint_id, user_id=user)
        
        # Store complaint info for logging
        complaint_issue = complaint.issue
        complaint_status = complaint.complaint_status
        
        # Only allow deletion if status is 'open' (prevent deletion of in-progress/resolved complaints)
        if complaint_status != 'open':
            logger.warning(f"Citizen {user.username} attempted to delete complaint #{complaint_id} with status: {complaint_status}")
            return JsonResponse({
                'success': False, 
                'message': f'Cannot delete complaint with status: {complaint_status}. Only open complaints can be deleted.'
            })
        
        # Delete the complaint
        complaint.delete()
        
        logger.info(f"Complaint #{complaint_id} ('{complaint_issue}') deleted by citizen {user.username}")
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True, 'message': 'Complaint deleted successfully!'})
        else:
            return redirect('citizen_dashboard')
            
    except Complaint.DoesNotExist:
        logger.warning(f"Citizen {user.username} attempted to delete non-existent or unauthorized complaint #{complaint_id}")
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'message': 'Complaint not found or unauthorized.'})
        else:
            return redirect('citizen_dashboard')
    except Exception as e:
        logger.error(f"Error deleting complaint #{complaint_id}: {str(e)}")
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'message': 'An error occurred while deleting the complaint.'})
        else:
            return redirect('citizen_dashboard')

# ADMIN DASHBOARD
def admin_dashboard(request):
    jwt_user = get_jwt_user(request)
    if not jwt_user or jwt_user[1] != 'admin':
        return redirect('login')
    user = jwt_user[0]

    # Get all complaints
    complaints = Complaint.objects.all().order_by('area_name', 'date_time')
    
    # Group complaints by area_name with statistics
    area_complaints = defaultdict(list)
    area_stats = {}
    
    for c in complaints:
        area_complaints[c.area_name].append(c)
    
    # Calculate statistics for each area
    for area, area_complaint_list in area_complaints.items():
        open_count = sum(1 for c in area_complaint_list if c.complaint_status == 'open')
        progress_count = sum(1 for c in area_complaint_list if c.complaint_status == 'in progress')
        resolved_count = sum(1 for c in area_complaint_list if c.complaint_status == 'resolved')
        
        area_stats[area] = {
            'total': len(area_complaint_list),
            'open': open_count,
            'progress': progress_count,
            'resolved': resolved_count
        }

    # Calculate overall statistics
    total_complaints = complaints.count()
    open_complaints = complaints.filter(complaint_status='open').count()
    progress_complaints = complaints.filter(complaint_status='in progress').count()
    resolved_complaints = complaints.filter(complaint_status='resolved').count()

    context = {
        'area_complaints': dict(area_complaints),
        'area_stats': area_stats,
        'total_complaints': total_complaints,
        'open_complaints': open_complaints,
        'progress_complaints': progress_complaints,
        'resolved_complaints': resolved_complaints,
        'user': user,
        'username': user.username,
        'email': user.email
    }

    return render(request, 'admin.html', context)

# EDIT COMPLAINT (FOR ADMINS)
def edit_complaint(request, complaint_id):
    jwt_user = get_jwt_user(request)
    if not jwt_user or jwt_user[1] != 'admin':
        return redirect('login')

    admin_user = jwt_user[0]  # Get the current admin user
    complaint = Complaint.objects.get(pk=complaint_id)

    if request.method == 'POST':
        old_status = complaint.complaint_status
        new_status = request.POST['complaint_status']
        
        # Only send notification if status actually changed
        if old_status != new_status:
            complaint.complaint_status = new_status
            complaint.save()
            
            # Send email notification to citizen about status change
            try:
                citizen = complaint.user_id
                email_sent = send_issue_status_change_mail(
                    citizen_email=citizen.email,
                    citizen_name=citizen.username,
                    complaint_id=complaint.complaint_id,
                    issue_title=complaint.issue,
                    old_status=old_status,
                    new_status=new_status
                )
                
                if email_sent:
                    logger.info(f"📧 Status change notification sent to {citizen.email} for complaint #{complaint.complaint_id}")
                    print(f"✅ Email notification sent to {citizen.username} about status change: {old_status} → {new_status}")
                else:
                    logger.warning(f"⚠️ Failed to send email notification to {citizen.email}")
                    print(f"⚠️ Failed to send email notification to {citizen.username}")
                    
            except Exception as e:
                logger.error(f"❌ Error sending status change notification: {str(e)}")
                print(f"❌ Error sending email notification: {str(e)}")
        else:
            complaint.save()
            
        return redirect('admin_dashboard')

    # If GET, show edit page
    return render(request, 'edit_complaint.html', {'complaint': complaint})
