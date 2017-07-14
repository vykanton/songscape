# Django settings for www project.
import os

DEBUG = True

ORG = "vuw"
SNIP_SUBSAMPLE_STEP = 1 #subsample step.  ie 4 is every 4th snippet of each recording.

ADMINS = (
    ('Edward Abraham', 'edward@dragonfly.co.nz'),
)

# This directory
PROJECT_DIR = os.path.dirname(__file__)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'songscape_dev',
        'USER': 'dba',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-nz'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

# Absolute filesystem path to the directory that will hold user-uploaded files.
RECORDINGS_ROOT = '/kiwi/recordings'
MEDIA_ROOT = os.path.join('/mnt/research_storage_snippets', 'media')

#Location the snippets will be written to.
SNIPPETS_PATH = '/mnt/research_storage_snippets/media/snippets'

# Absolute filesystem path to the directory that will hold species sample calls.
TRAINING_PATH = '/mnt/research_storage_snippets/sample_calls'

# Absolute filesystem path to the directory that will hold Neural network detectors.
DETECTOR_PATH = '/opt/songscape/detectors/'
HIHI_DETECTOR = DETECTOR_PATH+'hihi.pb'
KAKARIKI_DETECTOR = DETECTOR_PATH+'kakariki.pb'
TIEKE_DETECTOR = DETECTOR_PATH+'tieke.pb'

#Number of cores to use for the CNN detector.  Use a single core for high thoughput parallel computation.
DETECTOR_CORES = 1

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_DIR, '../static/')

STATICFILES_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        'APP_DIRS': True,
        # 'DEBUG': DEBUG,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
)

ROOT_URLCONF = 'www.urls'

LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
     'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'www.recordings',
    'django_nose',
    #'debug_toolbar',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [ '--with-xunit', '--with-doctest', ]

INTERNAL_IPS = ('127.0.0.1',)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            'filters': ['require_debug_false'],
        },
    }
}

RECORDINGS_PATH = '' # Path of the raw recordings

# organisation repositories. A dictionary with keys
# being the organisation codes, and values
# being the URLs of the servers that hold the
# raw recordings
#REPOSITORIES = {'RFPT': 'http://rfpt.songscape.org'}
REPOSITORIES = {'RFPT': 'http://192.168.0.123:8888'}

# Set your site url for security
SITE_URL = 'http://localhost:8000'


DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECT': False}

# Add the django_browserid authentication backend.
AUTHENTICATION_BACKENDS = (
   'django.contrib.auth.backends.ModelBackend', # required for admin
)


# Path to redirect to on successful login.
LOGIN_REDIRECT_URL = '/'

# Path to redirect to on unsuccessful login attempt.
LOGIN_REDIRECT_URL_FAILURE = '/'

# Path to redirect to on logout.
LOGOUT_REDIRECT_URL = '/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}



# Audio and sonogram quality settings
MAX_FRAMERATE = 24000
MIN_FREQ=000
MAX_FREQ=12000
N_FFT=512

# MEDIA_ROOT can be overridden in local_settings
SONOGRAM_DIR = 'sonograms/'
SNIPPET_DIR = 'snippets/'

try:
    from local_settings import *
except ImportError:
    print "Error loading local settings"
    pass


import sys
#if manage.py test was called, use test settings
if 'test' in sys.argv or 'migrationcheck' in sys.argv:
    try:
        from .test_settings import *
    except ImportError:
        print "Can't find test_settings.py"
