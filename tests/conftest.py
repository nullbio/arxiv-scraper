import pytest
from requests import Session
from unittest.mock import Mock
import logging
import re
import parse
from sql import SQL

# Define a list of URL regex matches to file paths
# fmt: off
url_file_mapping = [
    (re.compile(r"^https://arxiv.org/list/cs/1805$"), "tests/html/total_entries.html"),
    (re.compile(r"^https://example\.com/page2$"), "path/to/html/files/page2.html"),
    (re.compile(r"^https://example\.com/articles/\d+$"), "path/to/html/files/article.html"),
]
# fmt: on


@pytest.fixture
def logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger


# Mock the requests.get to return html files from disk instead.
# This way, we can create custom html files to cover weird edge cases.
def get_mock(url, *args, **kwargs):
    # Create a mock response object
    response_mock = Mock()

    # Find the matching file path based on the URL
    file_path = None
    for rgx, path in url_file_mapping:
        if rgx.match(url):
            file_path = path
            break

    if file_path:
        # Read the HTML file from disk
        with open(file_path, "r") as file:
            html_content = file.read()

        # Set the response content
        response_mock.text = html_content
        response_mock.status_code = 200
    else:
        # If no matching file path is found, raise an exception or set a default response
        raise Exception(f"No matching file path found for URL: {url}")
    return response_mock


@pytest.fixture
def session():
    sess = Session()
    sess.get = Mock(side_effect=get_mock)
    return sess


@pytest.fixture
def parser(session, logger):
    return parse.Parse(session, logger)


@pytest.fixture
def sql(logger):
    return SQL("arxiv_test.db", logger)
