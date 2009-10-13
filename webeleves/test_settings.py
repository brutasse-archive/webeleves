from settings import *

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = TEST_DATABASE_NAME = ':memory:'

CACHE_BACKEND = 'locmem:///'

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
    #'south',
    # 'Real' apps
    'website',
    'trombi',
    'photos',
    'forum',
)

TEST_RUNNER='coverage_runner.test_runner_with_coverage'

COVERAGE_MODULES = [
        'forum.views',
        'forum.models',
        'photos.models',
        'photos.views',
        'trombi.models',
        'trombi.views',
        'trombi.forms',
        'website.models',
        'website.views',
        'shortcuts',
]

# Gorun - get it at github.com/peterbe/gorun
# To use it: 'gorun test_settings.py'
DIRECTORIES = (
   ('forum',
    'python manage.py test forum photos trombi website --settings=test_settings'),
   ('photos',
    'python manage.py test forum photos trombi website --settings=test_settings'),
   ('trombi',
    'python manage.py test forum photos trombi website --settings=test_settings'),
   ('website',
    'python manage.py test forum photos trombi website --settings=test_settings'),
)
