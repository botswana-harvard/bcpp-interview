"""
WSGI config for x project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import site

from django.core.wsgi import get_wsgi_application

site.addsitedir('/Users/erikvw/.virtualenvs/bcpp-interview/lib/python3.5/site-packages')
site.addsitedir('/Users/erikvw/.virtualenvs/bcpp-interview/bin')

# VIRTUALENV_PATH = '/Users/erikvw/.virtualenvs/bcpp-interview/'
# ACTIVATE = os.path.join(VIRTUALENV_PATH, 'bin/activate_this.py')
# exec(open(ACTIVATE).read())
# execfile('path/to/activate_this.py', dict(__file__='path/to/activate_this.py'))
# sys.path.insert(0, os.path.join(VIRTUALENV_PATH, 'local/lib/python2.7/site-packages'))
# sys.path.insert(0, os.path.join(SOURCE_ROOT_PATH, LOCAL_PROJECT_RELPATH))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bcpp_interview.settings_apache")

application = get_wsgi_application()
