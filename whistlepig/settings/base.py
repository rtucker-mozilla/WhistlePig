# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *

# Name of the top-level module where you put all your apps.
# If you did not install Playdoh with the funfactory installer script
# you may need to edit this value. See the docs about installing from a
# clone.
PROJECT_MODULE = 'whistlepig'

# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

INSTALLED_APPS = list(INSTALLED_APPS) + [
    # Application base, containing global templates.
    '%s.base' % PROJECT_MODULE,
    '%s.whistlepig' % PROJECT_MODULE,
    '%s.api' % PROJECT_MODULE,
    '%s.admin_overrides' % PROJECT_MODULE,
    'django.contrib.admin',
    'django.contrib.auth',
    'django_browserid',
    'jingo_offline_compressor',
]

LOCALE_PATHS = (
    os.path.join(ROOT, PROJECT_MODULE, 'locale'),
)

# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = [
    'admin',
    'registration',
    'admin_overrides',
]

# BrowserID configuration
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_browserid.auth.BrowserIDBackend',
]

#SITE_URL = 'http://toolsdev2.dmz.scl3.mozilla.com:8099'
LOGIN_URL = '/en-US/admin/login/'
LOGIN_REDIRECT_URL = '/en-US/admin/whistlepig/statusupdate/'
LOGIN_REDIRECT_URL_FAILURE = '/en-US/admin/login/'

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'django_browserid.context_processors.browserid_form',
]

# Should robots.txt deny everything or disallow a calculated list of URLs we
# don't want to be crawled?  Default is false, disallow everything.
# Also see http://www.google.com/support/webmasters/bin/answer.py?answer=93710
ENGAGE_ROBOTS = False

# Always generate a CSRF token for anonymous users.
ANON_ALWAYS = True

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS['messages'] = [
    ('%s/**.py' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_python'),
    ('%s/**/templates/**.html' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_template'),
    ('templates/**.html',
        'tower.management.commands.extract.extract_tower_template'),
]

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# # Use this if you have localizable JS files:
# DOMAIN_METHODS['javascript'] = [
#    # Make sure that this won't pull in strings from external libraries you
#    # may use.
#    ('media/js/**.js', 'javascript'),
# ]
MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES) + [
    'whistlepig.middleware.securerequestpropogationmiddleware.SecureRequestPropagationMiddleware',
    ]

LOGGING = dict(loggers=dict(playdoh={'level': logging.DEBUG}))
def jinja_url(view_name, *args, **kwargs):
    from django.core.urlresolvers import reverse, NoReverseMatch
    try:
        return reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        try:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            return reverse(project_name + '.' + view_name,
                           args=args, kwargs=kwargs)
        except NoReverseMatch:
            return ''
def jinja_linebreaks(input_line):
    return input_line.replace("\n", "<br />")

import jinja2
jinja2.filters.FILTERS['url'] = jinja_url
jinja2.filters.FILTERS['linebreaks'] = jinja_linebreaks
CSP_SCRIPT_SRC = ("'self'", 'https://browserid.org','https://login.persona.org')
CSP_FRAME_SRC = ("'self'", 'https://browserid.org','https://login.persona.org')
TASTYPIE_DEFAULT_FORMATS = ['json']
BUGZILLA_URL = 'https://bugzilla.mozilla.org/show_bug.cgi?id='
