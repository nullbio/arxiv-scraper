import logging
from requests import Session
from requests_ratelimiter import LimiterAdapter

# Local modules
from scrape import Scrape
from request import Request
from sql import SQL

DATABASE_FILE = "arxiv.db"
DOWNLOAD_DIRECTORY = "arxiv_papers"
ERROR_LOG_FILE = "errors.txt"
LOG_FILE = "log.txt"
ARXIV_API_URL = "http://export.arxiv.org/api/query"
MAX_RESULTS_PER_REQUEST = 1000
SLEEP_TIME_BETWEEN_REQUESTS = 3  # seconds

withdraw_keywords = [
    "withdraw",
    "withdrew",
    "withdrawn",
    "retracted",
    "retract",
]


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
adapter = LimiterAdapter(per_second=4)
session.mount("http://", adapter)
session.mount("https://", adapter)
# set up the requests helper
request = Request(session, log)

# set up the scraper
scrape = Scrape(request, log, DOWNLOAD_DIRECTORY)

# set up the sqlite connection
sql = SQL(DATABASE_FILE, log)


__all__ = ["log", "scrape", "sql", "request"]
