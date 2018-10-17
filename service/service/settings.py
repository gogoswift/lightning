"""
Django settings for service project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import environ
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True),
    ALI_YUN_OSS_KEY=(str, ''),
    ALI_YUN_OSS_SECRET=(str, ''),
    ALI_YUN_OSS_ENDPOINT=(str, ''),
    ALI_YUN_OSS_HOST=(str, ''),
    ALI_YUN_OSS_BUCKET=(str, ''),
)
environ.Env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*7v=vsh$w@y!d=2qm4+9nvz#^mh63k@_!p2cp-j()v#%1#w9*b'


ALLOWED_HOSTS = ['*']

DEBUG = env('DEBUG')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'rest_framework',
    'rest_framework_swagger',
]

INTERNAL_APPS = [
    'member',
    'blog',
]

INSTALLED_APPS += THIRD_PARTY_APPS + INTERNAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'service.urls'

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

WSGI_APPLICATION = 'service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': env.db('DEFAULT_DATABASE', '')
}
DATABASES['default']['OPTIONS'] = {
    'charset': 'utf8mb4'
}
DATABASES['default']['TEST'] = {
    'CHARSET': 'utf8mb4',
    'COLLATION': 'utf8mb4_unicode_ci'
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'member.Author'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api_basebone.drf.handler.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'api_basebone.drf.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api_basebone.drf.authentication.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}


# 阿里云 OSS 配置
ALI_YUN_OSS_KEY = env('ALI_YUN_OSS_KEY')
ALI_YUN_OSS_SECRET = env('ALI_YUN_OSS_SECRET')
ALI_YUN_OSS_ENDPOINT = env('ALI_YUN_OSS_ENDPOINT')
ALI_YUN_OSS_HOST = env('ALI_YUN_OSS_HOST')
ALI_YUN_OSS_BUCKET = env('ALI_YUN_OSS_BUCKET')
