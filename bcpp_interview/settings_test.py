"""
Django settings for bcpp_interview project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys
from unipath import Path
from django.utils import timezone
from bcpp_interview.logging import LOGGING

from bcpp_interview.config import CORS_ORIGIN_WHITELIST, EDC_SYNC_ROLE
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
ETC_DIR = os.path.join(BASE_DIR.ancestor(1), 'etc')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(ETC_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_revision',
    'simple_history',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'django_js_reverse',
    'corsheaders',
    'crispy_forms',
    'edc_base',
    'edc_call_manager.apps.EdcCallManagerAppConfig',
    'edc_content_type_map.apps.EdcContentTypeAppConfig',
    'edc_device',
    'edc_identifier',
    'edc_map',
    'edc_locator',
    'call_manager',
    'edc_audio_recording.apps.EdcAudioRecordingAppConfig',
    'bcpp_interview.apps.DjangoCryptoFieldsAppConfig',
    'bcpp_interview.apps.EdcSyncAppConfig',
    'bcpp_interview.apps.EdcConsentAppConfig',
    'bcpp_interview.apps.BcppMapAppConfig',
    'bcpp_interview.apps.BcppInterviewAppConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'bcpp_interview.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'bcpp_interview.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR.ancestor(1), 'db.sqlite3'),
    }
}

# ssh -f -N -L 10000:127.0.0.1:5432 bcpp@getresults.bhp.org.bw
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'bcppi',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': '5432',  # 10000 if remote
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Gaborone'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR.ancestor(1).child('static')

MEDIA_ROOT = BASE_DIR.child('media')
MEDIA_URL = '/media/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


GIT_DIR = BASE_DIR.ancestor(1)
KEY_PATH = os.path.join(BASE_DIR.ancestor(1), 'crypto_fields')
SHOW_CRYPTO_FORM_DATA = True
STUDY_OPEN_DATETIME = timezone.datetime(2016, 1, 18)
LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'),
)

PROJECT_TITLE = 'Botswana Combination Prevention Project'
INSTITUTION = 'Botswana-Harvard AIDS Institute Partnership'
PROTOCOL_REVISION = '0.1dev'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
DEVICE_ID = '15'
SERVER_DEVICE_ID_LIST = ['99']
UPLOAD_FOLDER = os.path.join(MEDIA_ROOT, 'upload')
PROJECT_IDENTIFIER_PREFIX = '066'
CURRENT_SURVEY = 'bcpp-year-1'
CURRENT_COMMUNITY = None

CORS_ORIGIN_WHITELIST = CORS_ORIGIN_WHITELIST
REST_FRAMEWORK = {
    'PAGE_SIZE': 1,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
EDC_SYNC_ROLE = EDC_SYNC_ROLE

APP_LABEL = 'bcpp_interview'


# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# CSRF_COOKIE_HTTPONLY = True
