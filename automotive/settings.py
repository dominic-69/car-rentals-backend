"""
Django settings for automotive project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
import cloudinary

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = 'django-insecure-ruc9c^s!x7(dgl)5)2)-sn3%0=k=g+m^h99oo_g8j$o7a(rsf_'
DEBUG = True
ALLOWED_HOSTS = []

# Installed applications
INSTALLED_APPS = [
    'daphne',  # for channels

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'apps.users',
    'apps.cars',
    'apps.orders',
    'apps.rental',
    'apps.kyc',
    'apps.chat',
    'apps.sales',
    'apps.accessories',
    "apps.notifications",

    'corsheaders',
    'channels',
]

# Middleware configuration
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL, ASGI, and WSGI configuration
ROOT_URLCONF = 'automotive.urls'
WSGI_APPLICATION = 'automotive.wsgi.application'
ASGI_APPLICATION = "automotive.asgi.application"

# Channel Layers
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'car_rentals_db',
        'USER': 'dominic',
        'PASSWORD': 'dominic@1212',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Auth settings
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and Media files
STATIC_URL = 'static/'
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# JWT and Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'dominicproject96@gmail.com'
EMAIL_HOST_PASSWORD = 'eqjtjaspmcqbxjpm'

# Cloudinary configuration
cloudinary.config(
    cloud_name="de3aognnb",
    api_key="854385494215471",
    api_secret="QgR-koGGk9-24_cXsNp1UPtw6_I"
)

# Payment gateway settings
RAZORPAY_KEY_ID = "rzp_test_Sg7JEq3JdVsjLK"
RAZORPAY_KEY_SECRET = "Z0poo4BipmVFvGoAjcL31mjK"