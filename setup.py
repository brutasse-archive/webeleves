from setuptools import setup, find_packages

setup(
        name = 'webeleves',
        version = '0.1',
        packages = find_packages(),
        test_suite = 'webeleves.runtests.run_tests',
)
