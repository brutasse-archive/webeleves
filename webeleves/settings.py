# -*- coding: UTF-8 -*-
# Django settings for webeleves project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (u'Bruno Renié', 'bruno.renie@mines-saint-etienne.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wjdkl8)#$ay866$f7ev$_^%8gcfxyv%=j(h4am9w5n#a-b)1i1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'webeleves.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    # Cool libs
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'django.contrib.comments',
    'sorl.thumbnail',
    'south',
    # 'Real' apps
    'website',
    'trombi',
    'photos',
    'forum',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/' # if not {{ next }}
LOGOUT_URL = '/logout/'
AUTH_PROFILE_MODULE = 'trombi.UserProfile'

# LDAP settings
LDAP_SERVER = 'ldap://localhost'
LDAP_DATA = '' # Directory containing files with the output of ldapsearch

# French date format
DATE_FORMAT = 'd/m/Y'

THUMBNAIL_QUALITY = 100

AUTHENTICATION_BACKENDS = (
        # Default backend to LDAP backend
        'webeleves.auth.LDAPBackend',
        # Fallback to ModelBackend if needed
        'django.contrib.auth.backends.ModelBackend',
)

try:
    from local_settings import *
except ImportError:
    pass
