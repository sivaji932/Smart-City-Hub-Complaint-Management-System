# 🏛️ Smart City Hub - Municipal Complaint Management System

A comprehensive web-based platform for citizens to submit complaints and for administrators to manage and resolve municipal issues efficiently. Built with Django and Django REST Framework.

## ✨ Features

- 👥 **Multi-Role System**: Citizen, Admin, and Official roles
- 📝 **Complaint Management**: Submit, track, and manage complaints
- 📊 **Admin Dashboard**: Statistics, complaint overview, and management tools
- 📧 **Email Notifications**: 
  - Automatic alerts to admins for new complaints
  - Status update notifications to citizens
  - Professional email formatting with complaint details
- 🔐 **Secure Authentication**: Email-based login with JWT support
- 📱 **Responsive UI**: Modern, user-friendly interface
- 🗑️ **Complaint Management**: Citizens can delete their own complaints
- 📈 **Status Tracking**: Track complaints from submission to resolution

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)
- Gmail account with 2-Factor Authentication enabled (for email notifications)
- Git (for version control)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-city-hub.git
cd smart-city-hub/smart_hub
```

### 2. Set Up Virtual Environment

#### On Windows:
```bash
python -m venv env
.\env\Scripts\activate
```

#### On macOS/Linux:
```bash
python -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `smart_hub` directory by copying the template:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings
# On Windows: notepad .env
# On macOS/Linux: nano .env
```

### 5. Generate Django Secret Key (Important for Production)

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key and add it to your `.env` file:
```
DJANGO_SECRET_KEY=your-generated-secret-key-here
```

### 6. Initialize the Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account credentials.

### 8. Start the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## 📧 Email Configuration (Gmail SMTP)

The Smart Hub system includes automatic email notifications. Follow these steps to set up Gmail:

### Step 1: Enable 2-Factor Authentication on Gmail

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click on "Security" in the left sidebar
3. Scroll down to "How you sign in to Google"
4. Enable "2-Step Verification"
5. Complete the verification process

### Step 2: Generate an App Password

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Select "Mail" as the app
3. Select "Windows Computer" (or your device type)
4. Google will generate a 16-character password
5. **Copy this password** - you'll need it for the next step

### Step 3: Add Credentials to .env File

Edit your `.env` file and add/update:

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
ADMIN_EMAILS=admin1@example.com,admin2@example.com
```

### Step 4: Test Email Configuration

```bash
python test_gmail_email.py
```

This will test the email system and verify your configuration is correct.

## 🗂️ Project Structure

```
smart_hub/
├── complaint/                 # Main application
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   │   ├── admin.html       # Admin dashboard
│   │   ├── citizen.html     # Citizen dashboard
│   │   ├── official.html    # Official dashboard
│   │   ├── edit_complaint.html
│   │   └── login.html
│   ├── admin.py             # Django admin configuration
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # URL routing
│   ├── auth_backends.py     # Custom authentication
│   ├── email_utils.py       # Email utilities
│   └── utils.py             # Helper functions
├── smart_hub/               # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
├── EMAIL_SYSTEM_README.md  # Email system documentation
├── DEPLOYMENT.md           # Deployment guide
└── README.md              # This file
```

## 💾 Database Models

### Complaint Model
- **ID**: Unique identifier
- **Issue**: Title/summary of complaint
- **Description**: Detailed description
- **Area**: Location/area name
- **Category**: Complaint category
- **Status**: Complaint status (submitted, in-progress, resolved, closed)
- **Citizen**: Foreign key to citizen user
- **Date**: Submission timestamp
- **Documents**: Attached files (optional)

## 🔑 User Roles

### 👤 Citizen
- Register and login
- Submit new complaints
- View their complaint history
- Receive email notifications on status updates
- Delete their own complaints

### 👨‍💼 Admin
- View all complaints
- Change complaint status
- View statistics and analytics
- Manage officials
- Receive email notifications for new complaints

### 👮 Official
- View complaints in their area
- Update complaint status
- Provide resolution details

## 📖 Usage

### For Citizens:
1. Register or login to your account
2. Click "New Complaint"
3. Fill in the complaint details
4. Submit the complaint
5. Monitor status updates via email and dashboard

### For Admins:
1. Login to admin dashboard
2. View complaints in the main feed
3. Click on a complaint to view details
4. Update status and add comments
5. Click "Save Changes"
6. Citizen will automatically receive email notification

## 🛠️ Development

### Run Tests
```bash
python manage.py test
```

### Create Database Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Access Django Admin
Navigate to `http://127.0.0.1:8000/admin/` and login with your superuser credentials.

## 🔐 Security Considerations

- **Never commit `.env` file to version control** - it contains sensitive credentials
- **Use environment variables** for all sensitive configuration
- **Use a strong Django secret key** in production
- **Enable HTTPS** in production deployment
- **Set DEBUG=False** in production
- **Use a production-grade database** (PostgreSQL, MySQL) instead of SQLite
- **Keep dependencies updated** for security patches

## 📦 Dependencies

- Django 5.2.4 - Web framework
- djangorestframework 3.16.0 - REST API
- python-dotenv 1.1.1 - Environment variable management
- PyJWT 2.10.1 - JWT authentication
- requests 2.32.4 - HTTP requests library
- secure-smtplib 0.1.1 - Secure SMTP
- Other supporting libraries (see requirements.txt)

## 🚀 Deployment

### Production Checklist
- [ ] Generate a new Django SECRET_KEY
- [ ] Set DEBUG=False in .env
- [ ] Use a production database (PostgreSQL/MySQL)
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Set up proper logging
- [ ] Configure backups
- [ ] Use environment variables for all secrets

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🐛 Troubleshooting

### Email Not Sending
- Verify 2-Factor Authentication is enabled on Gmail
- Check that App Password is generated and correct
- Ensure ADMIN_EMAILS are correctly formatted in .env
- Run `python test_gmail_email.py` to test configuration
- Check logs in `smart_hub.log`

### Database Errors
- Ensure all migrations are applied: `python manage.py migrate`
- Delete `db.sqlite3` and rerun migrations if you get schema errors

### Virtual Environment Issues
- Ensure you've activated the virtual environment
- On Windows: `.\env\Scripts\activate`
- On macOS/Linux: `source env/bin/activate`

## 📞 Support

For issues, questions, or contributions:
1. Check existing documentation
2. Review [EMAIL_SYSTEM_README.md](EMAIL_SYSTEM_README.md) for email-specific issues
3. Check application logs in `smart_hub.log`
4. Create an issue in the repository

## 📝 License

This project is provided as-is for municipal complaint management.

## 👥 Contributors

- Project developed for Smart City Hub initiative

## 🔄 Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DJANGO_SECRET_KEY` | Secret key for Django | None | Yes (Prod) |
| `DEBUG` | Debug mode | True | No |
| `EMAIL_BACKEND` | Email backend type | django.core.mail.backends.smtp.EmailBackend | No |
| `EMAIL_HOST` | SMTP host | smtp.gmail.com | No |
| `EMAIL_PORT` | SMTP port | 587 | No |
| `EMAIL_USE_TLS` | Use TLS for SMTP | True | No |
| `EMAIL_HOST_USER` | SMTP username/email | Empty | For emails |
| `EMAIL_HOST_PASSWORD` | SMTP password/app password | Empty | For emails |
| `ADMIN_EMAILS` | Comma-separated admin emails | Empty | For admin notifications |

---

**Last Updated**: 2026  
**Status**: Production Ready
