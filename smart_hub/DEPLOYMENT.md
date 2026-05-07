# Smart Hub Deployment Guide

## 🚀 Quick Setup

### 1. Clone & Setup Environment
```bash
# Navigate to project directory
cd smart_hub

# Create virtual environment
python -m venv env

# Activate environment
# Windows:
.\env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the .env.example file to .env
cp .env.example .env

# Edit .env file with your settings
# Update Email credentials, secret key, and admin emails
nano .env  # or use your preferred editor
```

**Important Settings in .env:**
- `DJANGO_SECRET_KEY`: Generate a new secure key for production
- `DEBUG`: Set to False for production
- `EMAIL_HOST_USER`: Your Gmail address
- `EMAIL_HOST_PASSWORD`: Your Gmail app password
- `ADMIN_EMAILS`: Comma-separated list of admin emails

See [README.md](README.md) for detailed configuration instructions.


### 3. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin superuser (optional)
python manage.py createsuperuser
```

### 4. Run Application
```bash
# Start development server
python manage.py runserver

# Access at: http://127.0.0.1:8000/
```

## 📧 Email Configuration

### Gmail SMTP Setup:
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password for Mail
3. Add credentials to `.env` file (EMAIL_HOST_USER and EMAIL_HOST_PASSWORD)
4. Add admin emails to ADMIN_EMAILS in `.env` file

**See [README.md](README.md) for detailed Gmail setup steps.**


### Test Email System:
```bash
python test_gmail_email.py
```

## 🗂️ Project Structure
```
smart_hub/
├── complaint/          # Main app
│   ├── models.py      # Database models
│   ├── views.py       # Business logic
│   ├── email_utils.py # Email functionality
│   └── templates/     # HTML templates
├── smart_hub/         # Project settings
│   ├── settings.py    # Configuration
│   └── urls.py        # URL routing
├── requirements.txt   # Dependencies
└── manage.py         # Django management
```

## 🎯 Features
- ✅ Citizen complaint submission
- ✅ Admin dashboard with statistics
- ✅ Email notifications (new complaints → admins)
- ✅ Status update emails (changes → citizens)
- ✅ JWT authentication
- ✅ Modern responsive UI
- ✅ Complaint deletion (citizens)

## 🔐 Default Accounts
Create accounts through the signup/login interface or Django admin.