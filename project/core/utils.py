import logging
import time
from functools import wraps

from requests import Session
from requests.sessions import HTTPAdapter
from requests_ratelimiter import LimiterAdapter
from urllib3 import Retry


class ScrapeSession(Session):
    """Custom Session class to use for scraper http requests. ScrapeSession
    handles rate limiting with exponential backoff, automatic retries, and logging.

    Custom configurations can be supplied, or default settings can be used by
    initializing with no arguments.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, sleep_seconds=5, max_retries=5):
        # super().__init__()
        # self._decorate_methods()
        # TODO: Each plugin gets its own Session to use, and should persist it so its app/plugin wide.
        # TODO: set rate limiting per_host to true to track per host separately.
        # self.session = Session()
        # TODO: GET SETTINGS FROM ENV VARS OR DATABASE
        # TODO: STORE PLUGINS SETTINGS IN DATABASE FORM, SO THEY CAN BE ADJUSTED
        # VIA THE DJANGO ADMIN PANEL OR WEBSITE. MODEL INHERITANCE TO FORCE EXISTENCE.
        #
        # configure the requests session
        # Apply a rate-limit (4 requests per second) to all requests
        # As per guidance of Arxiv scraping recommendations in their docs
        #
        # adapter = LimiterAdapter(per_second=MAX_REQUESTS_PER_SECOND)
        # retries = Retry(
        #    total=5,
        #    backoff_factor=1,
        #    backoff_jitter=3,
        #    status_forcelist=[429, 500, 502, 503, 504], # same status codes for both adapters? 429 is too many requests and rest are server errors
        # )
        # retry_adapter = HTTPAdapter(max_retries=retries)

        # Setup rate limiting
        # rate_limiter = LimiterAdapter(per_second=3)

        # Mount both adapters
        # TODO: This wont work (double mounting), need to create a custom adapter class
        # like so: https://github.com/JWCook/requests-ratelimiter?tab=readme-ov-file#custom-session-example-requests-cache
        # which uses both the rate limiter and httpadapter
        # session.mount("http://", rate_limiter)
        # session.mount("https://", rate_limiter)
        # session.mount("http://", retry_adapter)
        # session.mount("https://", retry_adapter)
        super().__init__()
        self._decorate_methods()

        self.session = Session()
        self.log = logging.getLogger(__name__)
        self.sleep_seconds = sleep_seconds
        self.max_retries = max_retries

    def _decorate_methods(self):
        # Decorating the methods by redefining them
        for method_name in ["get", "post", "put", "delete", "head", "options", "patch"]:
            original_method = getattr(self, method_name)
            # Wrap the original method with the decorator
            decorated_method = self._handle_request(original_method)
            # Set the wrapped method
            setattr(self, method_name, decorated_method)

    def _handle_request(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.log.debug(f"Sending {func.__name__} request: {args}, {kwargs}")
                result = func(*args, **kwargs)
            except Exception as e:
                self.log.error(f"Error in {func.__name__}: {e}")
                raise
            return result

        return wrapper


_MAP = {
    "y": True,
    "yes": True,
    "t": True,
    "true": True,
    "on": True,
    "1": True,
    "n": False,
    "no": False,
    "f": False,
    "false": False,
    "off": False,
    "0": False,
    "": False,
}


def strtobool(value):
    try:
        return _MAP[str(value).lower()]
    except KeyError:
        raise ValueError('"{}" is not a valid bool value'.format(value))
