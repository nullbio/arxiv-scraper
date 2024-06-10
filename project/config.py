import logging

import django
from requests import Session
from requests_ratelimiter import LimiterAdapter

from project.core.utils.request import Request
from project.settings import *

# initialize django's settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

# set up the logger
log = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
# add a console logger handler
log.addHandler(logging.StreamHandler())

# error file handler
err_fh = logging.FileHandler(ERROR_LOG_FILE)
err_fh.setLevel(logging.ERROR)
log.addHandler(err_fh)

# configure the requests session
# Apply a rate-limit (4 requests per second) to all requests
# As per guidance of Arxiv scraping recommendations in their docs
session = Session()
adapter = LimiterAdapter(per_second=MAX_REQUESTS_PER_SECOND)
session.mount("http://", adapter)
session.mount("https://", adapter)
# set up the requests helper
request = Request(session, log)

# set up the sqlite connection
# sql = SQL(DATABASE_FILENAME, log)


__all__ = ["log", "request"]
