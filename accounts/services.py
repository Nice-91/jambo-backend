from datetime import datetime, timedelta
import jwt
from django.conf import settings
from .models import User, Device
from django.contrib.auth import authenticate


# -----------------------------
# JWT Authentication
# -----------------------------
def generate_jwt(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return token


def verify_jwt(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
        return user
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return None


# -----------------------------
# Device Verification
# -----------------------------
def verify_device(user, device_id):
    """
    Admin uses this to verify a user's device
    """
    try:
        device = Device.objects.get(user=user, device_id=device_id)
        device.is_verified = True
        device.save()
        return device
    except Device.DoesNotExist:
        return None


def is_device_verified(user, device_id):
    """
    Check if the device is verified before login
    """
    return Device.objects.filter(user=user, device_id=device_id, is_verified=True).exists()


# -----------------------------
# User Authentication
# -----------------------------
def authenticate_user(email, password, device_id=None):
    """
    Authenticate user and check if device is verified
    """
    user = authenticate(email=email, password=password)
    if not user:
        return None, "Invalid credentials"

    if device_id and not is_device_verified(user, device_id):
        return None, "Device not verified"

    token = generate_jwt(user)
    return token, None
