import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apikeymgr.settings")

application = get_wsgi_application()
