"""
Django settings for DMS project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from .config import *
import dj_database_url
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = "django-insecure-nouq*g&rwq0!df8w@)p*=34l$p(g%+!zf1g@sg_@zns^aa!vx-"

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG =  config('DEBUG',cast=bool)
DEBUG = True

# DEPLOY = not DEBUG ## Turn off debug mode in production
# HOST = True
HOST = False
CONFIG = get_config(HOST)

# ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(",")
ALLOWED_HOSTS = ['127.0.0.1', '*','cloud-vms.onrender.com']

DEFAULT_HASHING_ALGORITHM='sha1'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    # 'django_google.apps.DjangoGoogleConfig',
    ### for user authentication purpose ###
    "captcha",
    'accounts',

    ### our application list ####
    'vfms',
    # 'apptest',
    "pydrive",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  
]

ROOT_URLCONF = "DMS.urls"

# adding project_root to simplify migration to another system
PROJECT_ROOT=os.path.abspath(os.path.dirname(__file__))

TEMPLATES_DIR=(os.path.join(PROJECT_ROOT,'../templates'),)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR),'/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "DMS.context_process.media_path",
                "accounts.custom_auth.show_data"
              
            ],
        },
    },
]

WSGI_APPLICATION = "DMS.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases



database_name = 'vms_db' 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': database_name,
        # 'NAME': 'tms_product5',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Replace the SQLite DATABASES configuration with PostgreSQL:
# DATABASES = {
#     'default': dj_database_url.config(
#         # Replace this value with your local database's connection string.
#         default='postgresql://postgres:postgres@localhost:5432/DMS',
#         conn_max_age=600
#     )
# }

DATABASES['default']=dj_database_url.parse("postgres://videomanagement_user:ocPBcSfmrwlYyngZFxzUX87CkVwXKrFZ@dpg-cpdfvrvsc6pc739061o0-a.oregon-postgres.render.com/videomanagement")
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True 


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = '/static/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

    

## Media files (images) within django
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

## External to django storage
EXTERNAL_ROOT = os.path.join(CONFIG.EXTERNAL_BASEDIR,'external')
EXTERNAL_URL = '/external/'

## client uploaded videos stored path
DRIVE_ROOT = os.path.join(CONFIG.EXTERNAL_BASEDIR, 'UploadedVideos')
DRIVE_URL = '/UploadedVideos/'

### kindly place all the Detection videos in this path 
DETECTION_ROOT=os.path.join(CONFIG.EXTERNAL_BASEDIR, 'DetectionVideos')
DETECTION_URL ='/DetectionVideos/'

### kindly place all the sqllite files under this path
DETECTIONDB_ROOT=os.path.join(CONFIG.EXTERNAL_BASEDIR, 'sqllite')
DETECTIONDB_URL ='/sqllite/'

### kindly place all the detection vehicle count reports  under this path
CSVREPORT_ROOT=os.path.join(CONFIG.EXTERNAL_BASEDIR, 'CSVReports')
CSVREPORT_URL ='/CSVReports/'

GDRIVE_ROOT=os.path.join(CONFIG.EXTERNAL_BASEDIR, 'GWS')
GDRIVE_URL='/GWS/'

Gdrive_Folder='1-gc5Tv09ponupCxQu2pOE73EKk8OxUVC'
DAYS_THRESHOLD=21 #to delete google drive files older than 21 days ( 3weeks)

Video_File_Threshold='1 GB'

# print ("DRIVE_ROOT:", DRIVE_ROOT ,"DETECTIONDB_ROOT :", DETECTIONDB_ROOT)
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


