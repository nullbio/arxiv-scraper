from requests import Session
from requests_ratelimiter import LimiterAdapter
import parse as parse
import logging
from requester import Requester
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
logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
# add a console logger handler
logger.addHandler(logging.StreamHandler())

# error file handler
err_fh = logging.FileHandler(ERROR_LOG_FILE)
err_fh.setLevel(logging.ERROR)
logger.addHandler(err_fh)

# configure the requests session
# Apply a rate-limit (4 requests per second) to all requests
# As per guidance of Arxiv scraping recommendations in their docs
session = Session()
adapter = LimiterAdapter(per_second=4)
session.mount("http://", adapter)
session.mount("https://", adapter)
# set up the requests helper
requester = Requester(session, logger)

# set up the parser
parser = parse.Parse(requester, logger)

# set up the sqlite connection
sql = SQL(DATABASE_FILE, logger)


__all__ = ["logger", "parser", "sql", "requester", DOWNLOAD_DIRECTORY]
