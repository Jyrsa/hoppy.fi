# a bunch of settings for testing

from settings import *
#speed up tests 
SOUTH_TESTS_MIGRATE = False 
#don't leave a trace on the disk
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
}
#always eager should disable all 
#redis use but it's impossible to configure huey
#

HUEY = {
    'always_eager': True,
    'backend': 'huey.backends.redis_backend',  # required.
    }
