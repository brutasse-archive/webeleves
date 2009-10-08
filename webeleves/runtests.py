############################
### Making setup.py work ###
############################

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'webeleves.test_settings'

test_dir = os.path.join(os.path.dirname(__file__))
print "TEST", test_dir
sys.path.insert(0, test_dir)

from django.test.utils import get_runner
from django.conf import settings

def runtests():
    test_runner = get_runner(settings)
    failures = test_runner(
            ['forum', 'photos', 'trombi', 'website'],
            verbosity=1,
            interactive=True,
    )
    sys.exit(failures)

if __name__ == '__main__':
    runtests()

#######################
### End of setup.py ###
#######################
