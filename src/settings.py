# loaded from manage.py (if run manage.py), or config.py (if run main.py)
import os
from pathlib import Path

########
# GENERAL SETTINGS
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
DATABASE_FILENAME = "arxiv.db"
DATABASE_FILE_PATH = os.path.join(BASE_DIR, DATABASE_FILENAME)
DATABASE_CONNECTION = f"sqlite:///{DATABASE_FILE_PATH}"
DOWNLOAD_DIRECTORY = os.path.join(BASE_DIR, "arxiv_papers")
ERROR_LOG_FILE = os.path.join(BASE_DIR, "errors.txt")
LOG_FILE = os.path.join(BASE_DIR, "log.txt")
ARXIV_API_URL = "http://export.arxiv.org/api/query"
MAX_RESULTS_PER_REQUEST = 1000
SLEEP_TIME_BETWEEN_REQUESTS = 3  # seconds


WITHDRAW_KEYWORDS = [
    "withdraw",
    "withdrew",
    "withdrawn",
    "retracted",
    "retract",
]

########
# DJANGO SPECIFIC SETTINGS
# disable django's logger so our config.py logger can be used
INSTALLED_APPS = ("models",)

# We want to use our own logger, defined in config.py
LOGGING_CONFIG = None

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATABASE_FILE_PATH,
    }
}

# Set the secret key in your .env file.
SECRET_KEY = os.environ.get("SECRET_KEY")
