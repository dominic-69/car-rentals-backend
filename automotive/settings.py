"""
Django settings for automotive project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# 🔥 LOAD ENV
load_dotenv()

# =========================
# 📁 BASE DIR
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# 🔐 SECURITY
# =========================
SECRET_KEY = 'django-insecure-ruc9c^s!x7(dgl)5)2)-sn3%0=k=g+m^h99oo_g8j$o7a(rsf_'
DEBUG = True
ALLOWED_HOSTS = []

# =========================
# 🔥 APPLICATIONS
# =========================
INSTALLED_APPS = [
    'daphne',  # 🔥 MUST BE FIRST

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

    'corsheaders',
    'channels',
]

# =========================
# 🔥 MIDDLEWARE
# =========================
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

# =========================
# 🔥 URL / ASGI / WSGI
# =========================
ROOT_URLCONF = 'automotive.urls'

WSGI_APPLICATION = 'automotive.wsgi.application'

# ✅ 🔥 FIXED (IMPORTANT)
ASGI_APPLICATION = 'automotive.asgi.application'

# =========================
# 🔥 CHANNELS CONFIG
# =========================
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# =========================
# 🔥 TEMPLATES
# =========================
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

# =========================
# 🔥 DATABASE
# =========================
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

# =========================
# 🔐 AUTH
# =========================
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# 🌍 INTERNATIONAL
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =========================
# 📦 STATIC & MEDIA
# =========================
STATIC_URL = 'static/'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# =========================
# 🌐 CORS
# =========================
CORS_ALLOW_ALL_ORIGINS = True

# =========================
# 🔐 JWT
# =========================
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

# =========================
# 📧 EMAIL
# =========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'dominicproject96@gmail.com'
EMAIL_HOST_PASSWORD = 'eqjtjaspmcqbxjpm'

# =========================
# ☁️ CLOUDINARY
# =========================
import cloudinary

cloudinary.config(
    cloud_name="de3aognnb",
    api_key="854385494215471",
    api_secret="QgR-koGGk9-24_cXsNp1UPtw6_I"
)

# =========================
# 🤖 AI KEY
# =========================
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

RAZORPAY_KEY_ID = "rzp_test_Sg7JEq3JdVsjLK"
RAZORPAY_KEY_SECRET = "Z0poo4BipmVFvGoAjcL31mjK" 