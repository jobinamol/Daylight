from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key
import pymysql
from decouple import config
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from a .env file

BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = config('DJANGO_SECRET_KEY', default=get_random_secret_key())
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
# ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

ALLOWED_HOSTS = ['*']

# Razorpay API credentials
# settings.py
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

print("Razorpay Key ID:", RAZORPAY_KEY_ID)
print("Razorpay Key Secret:", RAZORPAY_KEY_SECRET)






SITE_ID = 2

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_extensions',# Required for Google login
    'resort',
    'userapp',
    'staffs',
    'adminpanal',
    'reservations',
    'bookings',
    'social_django',
]

# Add this line to specify the custom user model
AUTH_USER_MODEL = 'userapp.UserDB'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'key': '',  # This can usually be left blank unless you have specific requirements
        },
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'OAUTH_PKCE_ENABLED': True,  # Enable PKCE (Proof Key for Code Exchange) for security
    }
}
REDIRECT_URIS = [
    'http://127.0.0.1:8000/oauth/complete/google-oauth2/',
    'http://127.0.0.1:8000/accounts/google/login/callback/',
]




SOCIALACCOUNT_LOGIN_ON_GET = True

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Redirect settings
LOGIN_URL = '/accounts/google/login/'  # To initiate Google OAuth login
LOGIN_REDIRECT_URL = 'userindex'  # Redirect after successful login
LOGOUT_REDIRECT_URL = 'home'  # Redirect after logout
 # This triggers Google login

# Allauth settings
AUTH_USER_MODEL = 'userapp.UserDB'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_FIELD = 'emailid'  # Change this to 'emailid'


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_ADAPTER = 'userapp.adapters.CustomSocialAccountAdapter'

LOGIN_REDIRECT_URL = '/userindex/'  # Adjust this to your desired redirect URL after login
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Google OAuth2 configuration for Django Allauth


# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Ensure this is included
]

ROOT_URLCONF = 'daycation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'daycation.wsgi.application'

# MySQL Database Configuration
pymysql.install_as_MySQLdb()

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv('DB_NAME', 'DRMS'),
#         'USER': os.getenv('DB_USER', 'jobina'),
#         'PASSWORD': os.getenv('DB_PASSWORD', '1234'),
#         'HOST': os.getenv('DB_HOST', 'localhost'),
#         'PORT': os.getenv('DB_PORT', '3306'),
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#         },
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DRMS_kitchenwe',
        'USER': 'DRMS_kitchenwe',
        'PASSWORD': 'e63c87edeef1a253b38a633793929686772a708a',
        'HOST': 'w5mbd.h.filess.io',
        'PORT': '3307',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'jobinamoljaimon2025@mca.ajce.in')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'Jaimon@123*')  # Store in .env file for security
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'jobinamoljaimon2025@mca.ajce.in')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
}
