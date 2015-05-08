"""
Django settings for website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'ts3$31g4d2rc=&g+elh&b4m^5=pz!87(v^)nk1p&e917cp-*w('

DEBUG = True
#DEBUG = False
TEMPLATE_DEBUG = DEBUG
if DEBUG: ALLOWED_HOSTS = []
else:ALLOWED_HOSTS=['*']


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrapform',
    #----------------
    'question',
    'contest',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'website.urls'
WSGI_APPLICATION = 'website.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = None
USE_I18N = False
USE_L10N = False
USE_TZ = False

STATIC_URL = '/static/'
MEDIA_URL='/media/'
STATIC_ROOT=os.path.join(BASE_DIR,'static_files')
MEDIA_ROOT=os.path.join(STATIC_ROOT,'media_files')

TEMPLATE_DIRS=[os.path.join(BASE_DIR,'templates')]
STATICFILES_DIRS=[os.path.join(BASE_DIR,'staticfiles')]
LOGIN_REDIRECT_URL='/'
LOGIN_URL='/login/'

CHECK_SERVER_ADDRESS=('127.0.0.1',9000)
