from settings import *

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = TEST_DATABASE_NAME = ':memory:'

CACHE_BACKEND = 'locmem:///'

TEST_RUNNER='coverage_runner.test_runner_with_coverage'

COVERAGE_MODULES = [
        'forum.views',
        'forum.models',
        'photos.models',
        'photos.views',
        'trombi.models',
        'trombi.views',
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
