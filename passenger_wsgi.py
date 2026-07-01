import os

# Replace 'myproject' with your actual Django project folder name
os.environ['DJANGO_SETTINGS_MODULE'] = 'ragwud.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()