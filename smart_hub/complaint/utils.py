import jwt
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password

SECRET_KEY = settings.SECRET_KEY

def create_jwt(user):
    payload = {
        'user_id': user.user_id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None