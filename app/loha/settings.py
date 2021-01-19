"""
Django settings for loha project.

Generated by 'django-admin startproject' using Django 2.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os, json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

# Keep secret keys in secrets.json
def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        return None


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(get_secret("DEBUG"))

#SECRET_KEY
# IAMPORT
IAMPORT_CODE=get_secret('IAMPORT_CODE')
IAMPORT_REST_KEY=get_secret('IAMPORT_REST_KEY')
IAMPORT_SECRET_REST_KEY=get_secret('IAMPORT_SECRET_REST_KEY')
# CLAYFUL
CLAYFUL_SECRET_KEY=get_secret('CLAYFUL_SECRET_KEY')
# KAKAO
KAKAO_APP_ID=get_secret('KAKAO_APP_ID')
KAKAO_REST_API=get_secret('KAKAO_REST_API')
KAKAO_ADMIN_KEY=get_secret('KAKAO_ADMIN_KEY')
# NAVER
NAVER_CLIENT_ID=get_secret('NAVER_CLIENT_ID')
NAVER_SECRET_KEY=get_secret('NAVER_SECRET_KEY')
# MUX
MUX_CLIENT_ID = get_secret('MUX_CLIENT_ID')
MUX_SECRET_KEY = get_secret('MUX_SECRET_KEY')

# HOST
ALLOWED_HOSTS = get_secret("DJANGO_ALLOWED_HOSTS")
# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'user',
    'product',
    'category',
    'wishlist',
    'cart',
    'payment',
    'usergroup',
    'images',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'loha.urls'

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

WSGI_APPLICATION = 'loha.wsgi.application'


# development settings
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': get_secret('APP_DB_ENGINE') or 'django.db.backends.sqlite3',
        'NAME': get_secret('DB_NAME') or os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': get_secret('DB_USER') or '',
        'PASSWORD': get_secret('PASSWORD') or '',
        'HOST': get_secret('HOST') or None,
        'PORT': get_secret('PORT') or None,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ko-kr'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# 창 닫으면 로그아웃
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Datetime format
DATETIME_FORMAT = 'Y-m-d H:i:s'
