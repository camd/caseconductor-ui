# Case Conductor is a Test Case Management system.
# Copyright (C) 2011 uTest Inc.
# 
# This file is part of Case Conductor.
# 
# Case Conductor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Case Conductor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Case Conductor.  If not, see <http://www.gnu.org/licenses/>.
"""
Default Django settings for ccui project.

"""
from os.path import dirname, join, abspath

BASE_PATH = dirname(dirname(dirname(abspath(__file__))))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = [
    ("Carl Meyer", "cmeyer@mozilla.com"),
]

MANAGERS = ADMINS

# Just to avoid deprecation warnings
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(BASE_PATH, "collected-assets")

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

MEDIA_ROOT = join(BASE_PATH, "media")

MEDIA_URL = "/media/"

# A list of locations of additional static files
STATICFILES_DIRS = [join(BASE_PATH, "static")]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don"t share it with anybody.
SECRET_KEY = "override this"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages"
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "djangosecure.middleware.SecurityMiddleware",
    "ccui.core.middleware.StaticCompanyMiddleware",
    "ccui.users.middleware.AuthenticationMiddleware",
    "ccui.environments.middleware.EnvironmentsMiddleware",
]

ROOT_URLCONF = "ccui.urls"

TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don"t forget to use absolute paths, not relative paths.
    join(BASE_PATH, "templates"),
]

DATE_FORMAT = "Y-m-d"

INSTALLED_APPS = [
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ccui.core",
    "ccui.static",
    "ccui.users",
    "ccui.products",
    "ccui.environments",
    "ccui.testexecution"
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request":{
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

INSTALLED_APPS += ["compressor"]
COMPRESS_CSS_FILTERS = ["compressor.filters.css_default.CssAbsoluteFilter",
                        "ccui.compressor_filters.SlimmerCSSFilter"]

INSTALLED_APPS += ["floppyforms"]

INSTALLED_APPS += ["djangosecure"]
SESSION_COOKIE_HTTPONLY = True
SECURE_FRAME_DENY = True

INSTALLED_APPS += ["icanhaz"]
ICANHAZ_DIRS = [join(BASE_PATH, "jstemplates")]

INSTALLED_APPS += ["html5accordion"]

INSTALLED_APPS += ["messages_ui"]
MIDDLEWARE_CLASSES.insert(
    MIDDLEWARE_CLASSES.index(
        "django.contrib.messages.middleware.MessageMiddleware"
        ) + 1,
    "messages_ui.middleware.AjaxMessagesMiddleware")

INSTALLED_APPS += ["ajax_loading_overlay"]

CC_API_BASE = "http://localhost:8080/tcm/services/v2/rest/"
CC_ADMIN_USER = "admin@utest.com"
CC_ADMIN_PASS = "admin"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "runtests"
