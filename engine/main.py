import datetime
import os
import runpy
import time
import traceback
from django.db import connection
from django.core.wsgi import get_wsgi_application

import jose_cuervo.settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jose_cuervo.settings")

application = get_wsgi_application()



def mainEngine():
   while(True):
      print('Hello World!!')

mainEngine()