import glob
import importlib.util
import logging
import re
from pathlib import Path
from unittest.mock import Mock

import pytest
from django.core.management import call_command
from plugins import arxiv

import project.settings as settings
from project.core.utils import ScrapeSession

# Local modules
from project.plugins.arxiv.parse import Parse
from project.plugins.arxiv.scrape import Scrape

tests_path = Path(__file__).resolve().parent
tests_path = settings.BASE_DIR / "project/plugins/arxiv/tests"
core_fixtures_path = settings.BASE_DIR / "project/core/fixtures"

# Define a list of URL regex matches to file paths
url_file_mapping = [
    (
        re.compile(r"^https://arxiv.org/list/cs/1805$"),
        f"{tests_path}/html/total_entries.html",
    ),
    (
        re.compile(r"^https://example\.com/page2$"),
        f"{tests_path}/html/page2.html",
    ),
    (
        re.compile(r"^https://example\.com/articles/\d+$"),
        f"{tests_path}/html/article.html",
    ),
]


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
        # If no matching file path is found,
        # raise an exception or set a default response
        raise Exception(f"No matching file path found for URL: {url}")
    return response_mock


@pytest.fixture(scope="function")
def reload_model_fixtures():
    """Because we're using pytest instead of unittest, we have to load our model
    fixtures manually. This fixture reloads the model fixtures after every test,
    provided the test has a @pytest.mark.django_db decorator and the test class
    defines a @pytest.fixture(autouse=True) method that takes this fixture as an arg.
    """
    arxiv_fixtures_path = f"{tests_path}/../fixtures"
    core_fixtures = glob.glob(f"{core_fixtures_path}/*.json")
    arxiv_fixtures = glob.glob(f"{arxiv_fixtures_path}/*.json")
    assert len(arxiv_fixtures) > 0, f"No arxiv fixtures found in {arxiv_fixtures_path}"
    assert len(core_fixtures) > 0, f"No core fixtures found in {core_fixtures_path}"
    for fixture in core_fixtures:
        call_command("loaddata", fixture)

    for fixture in arxiv_fixtures:
        call_command("loaddata", fixture)


@pytest.fixture(scope="class")
def log():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    return log


@pytest.fixture
def session(log):
    sess = ScrapeSession()
    sess.get = Mock(side_effect=get_mock)
    return sess


@pytest.fixture
def parse(log):
    return Parse(log)


@pytest.fixture
def scrape(session, log):
    return Scrape(session, log, "MOCK_DOWNLOAD_DIR")
