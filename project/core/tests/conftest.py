import glob

import pytest
from django.core.management import call_command

import project.settings as settings

core_fixtures_path = settings.BASE_DIR / "project/core/fixtures"


@pytest.fixture(scope="function")
def reload_model_fixtures():
    """Because we're using pytest instead of unittest, we have to load our model
    fixtures manually. This fixture reloads the model fixtures after every test,
    provided the test has a @pytest.mark.django_db decorator and the test class
    defines a @pytest.fixture(autouse=True) method that takes this fixture as an arg.
    """
    core_fixtures = glob.glob(f"{core_fixtures_path}/*.json")
    assert len(core_fixtures) > 0, f"No core fixtures found in {core_fixtures_path}"
    for fixture in core_fixtures:
        call_command("loaddata", fixture)
