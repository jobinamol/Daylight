import pyotp
import logging
from django.core.mail import send_mail
from django.conf import settings
from .models import UserDB  # Import your UserDB model

# Configure logging
logger = logging.getLogger(__name__)

def generate_otp(user):
    """
    Generate a one-time password (OTP) for the user based on their OTP secret.
    """
    if not user.otp_secret:
        # Generate a new OTP secret if not available
        user.otp_secret = pyotp.random_base32()
        user.save()

    totp = pyotp.TOTP(user.otp_secret)  # Create a TOTP object using the user's OTP secret
    return totp.now()  # Generate the OTP


def send_otp_to_user(user, otp):
    """
    Send OTP to the user's registered email.
    """
    subject = "Your OTP Code"
    message = f"Your OTP code is {otp}. It is valid for a short time."
    from_email = settings.DEFAULT_FROM_EMAIL  # Ensure this is configured in settings
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Error sending OTP email to {user.email}: {e}")
        return False


def generate_and_send_otp(user):
    """
    Generate and send OTP to the user.
    """
    otp = generate_otp(user)
    if send_otp_to_user(user, otp):
        return otp  # Optionally, return the OTP for debugging/testing purposes
    return None
