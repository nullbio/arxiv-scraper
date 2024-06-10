import os
from pathlib import Path

from project.core.utils.utils import strtobool

##############################
# PROJECT SPECIFIC SETTINGS
##############################

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # project root

# Environment variables
DOWNLOAD_DIRECTORY = os.environ.get(
    "DOWNLOAD_DIRECTORY", os.path.join(BASE_DIR, "arxiv_papers")
)

DATABASE_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "arxiv.db"))
DATABASE_CONNECTION = f"sqlite:///{DATABASE_PATH}"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": DATABASE_PATH}}

LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING")
LOG_FILE = os.environ.get("LOG_FILE", os.path.join(BASE_DIR, "log.txt"))
ERROR_LOG_FILE = os.environ.get("ERROR_LOG_FILE", os.path.join(BASE_DIR, "errors.txt"))

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

DEBUG = strtobool(os.environ.get("DEBUG", False))

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

# disable django's logger so our config.py logger can be used.
# We want to use our own logger, defined in config.py
LOGGING_CONFIG = None

# Default automatic id field generation for models
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "plugins.arxiv",
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
