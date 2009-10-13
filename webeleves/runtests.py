############################
### Making setup.py work ###
############################

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'webeleves.test_settings'
APPS = ['website', 'photos', 'trombi', 'forum']

test_dir = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, test_dir)

from django.test.utils import get_runner
from django.conf import settings
from django.test.utils import setup_test_environment, teardown_test_environment
from django.test.simple import build_suite, reorder_suite
from django.test.testcases import TestCase
from django.db.models import get_app, get_apps

from bitten.util.testrunner import XMLTestRunner
import unittest

def run_tests(test_labels=APPS, verbosity=1, interactive=True, extra_tests=[]):
    """Hack on top of django.test.simple.run_tests to use the XML test runner
    provided by Bitten"""
    setup_test_environment()
    settings.DEBUG = False
    suite = unittest.TestSuite()

    if test_labels:
        for label in test_labels:
            if '.' in label:
                suite.addTest(build_test(label))
            else:
                app = get_app(label)
                suite.addTest(build_suite(app))
    else:
        for app in get_apps():
            suite.addTest(build_suite(app))

    for test in extra_tests:
        suite.addTest(test)

    suite = reorder_suite(suite, (TestCase,))
    old_name = settings.DATABASE_NAME
    from django.db import connection
    connection.creation.create_test_db(verbosity, autoclobber=not interactive)
    result = XMLTestRunner(stream=sys.stdout, xml_stream=open('test-results.xml', 'w')).run(suite)
    connection.creation.destroy_test_db(old_name, verbosity)

    teardown_test_environment()

    return result

#######################
### End of setup.py ###
#######################
