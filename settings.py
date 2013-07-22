# Django settings for gismon project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Cristian Salamea', 'cristian.salamea@gnuthink.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'gismon_empty'             # Or path to database file if using sqlite3.
DATABASE_USER = 'ovnicraft'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Guayaquil'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ec'

SITE_ID = 1
GOOGLE_MAPS_API_KEY  = 'ABQIAAAAZJAxdUVOaDDgn3nLQQYuyRQ7ewXWfe-qAGN7fhHFFe0sU51e7hS-SKZfZ7ktS40xR0GJa2kxqtcEbQ'

#GOOGLE_MAPS_API_KEY = 'ABQIAAAAZJAxdUVOaDDgn3nLQQYuyRT2yXp_ZAY8_ufC3CFXhHIE1NvwkxSPl7SvNZianMwwPK9FBmnelRJk6g'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = ''

import os.path

STATIC_MEDIA = os.path.normpath(os.path.join(os.path.dirname(__file__), 'gis/site_media'))

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#7oq*x7mds%lwof)t&e8edl6qet$ri63lnl6jv)@je^9da$njt'

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

ROOT_URLCONF = 'gismon.urls'



TEMPLATE_DIRS = (
    os.path.normpath(os.path.join(os.path.dirname(__file__), 'templates')),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.gis',
    'gismon.entergis',
#    'gismon.compressor',
)


