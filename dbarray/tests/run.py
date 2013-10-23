"""From http://stackoverflow.com/a/12260597/400691"""
import sys

from django.conf import settings


settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dbarray',
            'HOST': 'localhost'
        }
    },
    INSTALLED_APPS=(
        'dbarray.tests',
        # 'django.contrib.auth',
        # 'django.contrib.contenttypes',
        # 'django.contrib.sessions',
        # 'django.contrib.admin',
    ),
)

from discover_runner import DiscoverRunner

test_runner = DiscoverRunner(verbosity=1)
failures = test_runner.run_tests(['dbarray'])
if failures:
    sys.exit(1)
