import os
from pathlib import Path

import dotenv

from project.core.utils import strtobool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # project root

##############################
# Load the .env vars
##############################
ENV_FILE_PATH = BASE_DIR / ".env"
dotenv.load_dotenv(str(ENV_FILE_PATH))

##############################
# PROJECT SPECIFIC SETTINGS
##############################

DEBUG = strtobool(os.environ.get("DEBUG", False))

AVAILABLE_PLUGINS = [
    ("Arxiv", "project.plugins.arxiv"),
]

DOWNLOAD_DIRECTORY = os.environ.get(
    "DOWNLOAD_DIRECTORY", os.path.join(BASE_DIR, "documents")
)

DATABASE_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "scrapii.db"))
DATABASE_CONNECTION = f"sqlite:///{DATABASE_PATH}"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": DATABASE_PATH}}

LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG" if DEBUG else "WARNING")
LOG_FILE = os.environ.get("LOG_FILE", os.path.join(BASE_DIR, "general.log"))
ERROR_LOG_FILE = os.environ.get("ERROR_LOG_FILE", os.path.join(BASE_DIR, "errors.log"))

# Force range between 1 and 2000
max_results_per_request = int(os.environ.get("MAX_RESULTS_PER_REQUEST", 2000))
MAX_RESULTS_PER_REQUEST = (
    max_results_per_request
    if max_results_per_request > 0 and max_results_per_request <= 2000
    else 2000
)

# Set a hard cap of 10 requests per second to prevent abuse.
max_requests_per_second = float(os.environ.get("MAX_REQUESTS_PER_SECOND", 1.0))
MAX_REQUESTS_PER_SECOND = (
    max_requests_per_second
    if max_requests_per_second <= 10.0 and max_requests_per_second > 0.0
    else 1.0
)

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("SECRET_KEY is not set in .env file.")
elif SECRET_KEY == "<your secret key>":
    raise Exception("Invalid SECRET_KEY value in your .env file, please change it.")

ALL_CATEGORIES = [
    "astro-ph",
    "cond-mat",
    "gr-gc",
    "hep-ex",
    "hep-lat",
    "hep-ph",
    "hep-th",
    "math-ph",
    "nlin",
    "nucl-ex",
    "nucl-th",
    "physics",
    "quant-ph",
    "math",
    "cs",
    "q-bio",
    "q-fin",
    "stat",
    "eess",
    "econ",
]

enabled_categories = os.environ.get("ENABLED_CATEGORIES", "").strip(" ").split(",")
ENABLED_CATEGORIES = (
    enabled_categories if len(enabled_categories) > 0 else ALL_CATEGORIES
)

ARXIV_API_URL = "http://export.arxiv.org/api/query"

WITHDRAW_KEYWORDS = [
    "withdraw",
    "withdrew",
    "withdrawn",
    "retracted",
    "retract",
]

########################################
# DJANGO SPECIFIC SETTINGS BELOW
########################################

INSTALLED_APPS = ("core",)

LOGGING = {
    "version": 1,  # the dictConfig format version
    "disable_existing_loggers": False,  # retain the default loggers
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "general": {
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "level": LOG_LEVEL,
            "formatter": "standard",
        },
        "errors": {
            "class": "logging.FileHandler",
            "filename": ERROR_LOG_FILE,
            "level": "ERROR",
            "formatter": "standard",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {
            "level": LOG_LEVEL,
            "handlers": ["general", "errors", "console"],
        },
    },
}

# Default automatic id field generation for models
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Core app (initialises plugins)
    "project.core",
    # Scraper plugins
    "project.plugins.arxiv",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"
TIME_ZONE = "UTC"
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"


###############################
# Celery settings
###############################

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
