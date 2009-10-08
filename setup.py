from setuptools import setup, find_packages

#import os, sys
#project = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.insert(0, project)

setup(
        name = 'webeleves',
        version = '0.1',
        packages = find_packages(),
        test_suite = 'webeleves.runtests.runtests',
)
