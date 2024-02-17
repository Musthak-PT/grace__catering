"""
Django settings for root_project_django_v4 project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import os
import secrets
from celery.schedules import crontab

load_dotenv() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')
E_COMMERCE_SECRET = os.environ.get('E_COMMERCE_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.environ.get('DEBUG', '')
DEBUG = True if os.environ.get("DEBUG_VALUE", "").lower() == 'true' else False
ALLOWED_HOSTS = [
    '127.0.0.1',
    'https://solo-api.aventusinformatics.com',
    '*',
]

CSRF_TRUSTED_ORIGINS  = [
    "http://127.0.0.1:8000",
    "https://solo-api.aventusinformatics.com",
]


CORS_ALLOWED_ORIGINS  = [
    "http://127.0.0.1",
    "https://solo-api.aventusinformatics.com",
]

CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# local appications
LOCAL_APPS = [
    'apps.users',
    'apps.home',
    'apps.admins',
    'apps.category',
    'apps.product',
    'apps.user_management',
    'apps.order',
]

# additional plugin apps
THIRD_PARTY_APPS = [
    'drf_yasg',
    'rest_framework_simplejwt',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'django_acl',
    'django_celery_beat',
    'django_celery_results',
]


INSTALLED_APPS = INSTALLED_APPS + LOCAL_APPS + THIRD_PARTY_APPS


TABLE_PREFIX = 'solo_core__'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "apps.review.middleware.RequestMiddleware",
]

ROOT_URLCONF = 'solo_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'solo_core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TIME_ZONE', 'Asia/Kolkata')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_URL = 'assets/'
STATIC_ROOT  = os.path.join(BASE_DIR, 'assets')
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'),
)



MEDIA_URL = "/media/"
MEDIA_ROOT =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'






#Additional
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


LOGIN_URL = '/auth/login'

AUTH_USER_MODEL = 'users.Users'

PROJECT_NAME = 'solo_core'


DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000000


SWAGGER_SETTINGS = {
    'DEFAULT_API_URL' : os.environ.get('SWAGGER_DEFAULT_API_URL', ""),
    
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Basic': {
                'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    
}


REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'solo_core.exceptions.handle_exception',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',
    ),
    
}

SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=2),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'eShVmYq3t6w9z$C&E)H@McQfTjWnZr4u7x!A%D*G-JaNdRgUkXp2s5v8y/B?E(H+',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=60),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=90),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


ENCRYPTION_SECRET_KEY = 'hWmZq4t7w!z$C&F)J@NcRfUjXn2r5u8x/A?D*G-KaPdSgVkYp3s6v9y$B&E)H+Mb'


SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

""" EMAIL CONFIGURATIONS"""

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_DOMAIN = os.environ.get('EMAIL_DOMAIN')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'
ADMIN_FORGOT_PASSWORD_PAGE_URL=os.environ.get('ADMIN_FORGOT_PASSWORD_PAGE_URL')
CUSTOMER_FORGOT_PASSWORD_PAGE_URL=os.environ.get('CUSTOMER_FORGOT_PASSWORD_PAGE_URL')

"""ADMIN MAIL FOE CONTACT US"""
ADMIN_MAIL                = os.environ.get('ADMIN_MAIL')
UNSUBSCRIPTION_PATH       = os.environ.get('UNSUBSCRIPTION_PATH')
BLOG_DETAILS_VIEW_PATH    = os.environ.get('BLOG_DETAILS_VIEW_PATH')
GET_CANDIDATE_CV_PATH     = os.environ.get('GET_CANDIDATE_CV_PATH')


if 'EMAIL_SENDER_NAME' in os.environ:
    EMAIL_SENDER_NAME = os.environ.get('EMAIL_SENDER_NAME')
else:
    EMAIL_SENDER_NAME = 'Solo'



DEFAULT_DECIMAL_PLACES = 3
DEFAULT_MAX_DIGITS = 12



# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_TIMEZONE = 'Asia/Kolkata'


# CELERY_BROKER_TRANSPORT_OPTIONS = {
#     'region': 'us-east-1',  # Replace this with your preferred AWS region
#     'polling_interval': 20,
#     'visibility_timeout': 3600,  # Optional: adjust the timeout as per your needs
# }



# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",  # Replace with your Redis server details
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# # CELERY_BEAT_SCHEDULE = {
# #     'auto_review_email': {
# #         'task': 'apps.review.tasks.auto_review_email',
# #         'schedule': crontab(hour=11, minute=0),
# #     }
# # }
# CELERY_BEAT_SCHEDULE = {
#     'auto_review_email': {
#         'task': 'apps.review.tasks.auto_review_email',
#         'schedule': crontab(minute='*/5'),  # Run every 5 minutes
#     }
# }


# Celery settings
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL',"redis://127.0.0.1:6379")
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_RESULT_BACKEND = "django-db"

CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': 'us-east-1',  # Replace this with your preferred AWS region
    'polling_interval': 20,
    'visibility_timeout': 3600,  # Optional: adjust the timeout as per your needs
}

# result_serializer = 'json'

#celery beat
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'