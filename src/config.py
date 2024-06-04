from requests import Session
from requests_ratelimiter import LimiterAdapter
import parse as parse
import logging
from sql import SQL

DATABASE_FILE = "arxiv.db"
DOWNLOAD_DIRECTORY = "arxiv_papers"
ERROR_LOG_FILE = "errors.txt"
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

# Use this for requests
session = Session()
# Apply a rate-limit (4 requests per second) to all requests
# As per guidance of Arxiv scraping recommendations in their docs
adapter = LimiterAdapter(per_second=4)
session.mount("http://", adapter)
session.mount("https://", adapter)

# set up the logger
logger = logging.getLogger(__name__)

logging.basicConfig(filename="log.txt", level=logging.DEBUG)

# add a console logger handler
logger.addHandler(logging.StreamHandler())

# set up the parser
parser = parse.Parse(session, logger)

# set up the sqlite connection
sql = SQL(DATABASE_FILE, logger)
