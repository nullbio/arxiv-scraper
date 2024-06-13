import pytest

import project.core.models as models


class TestModels:
    @pytest.fixture(autouse=True)
    def reload_model_fixtures(self, reload_model_fixtures):
        # Reload the model fixtures after every test
        pass

    @pytest.mark.django_db
    def test_category_fixtures(self):
        c = models.Category.objects.all()
        # Should be 11 categories
        assert len(c) == 11

        expected_names = ["wrong"]
        intersect = set(expected_names).intersection(set([row.name for row in c]))
        # Check negative case
        assert len(intersect) != len(expected_names)

        expected_names = [
            "cond-mat",
            "math-ph",
            "nlin",
            "physics",
            "math",
            "cs",
            "q-bio",
            "q-fin",
            "stat",
            "eess",
            "econ",
        ]

        intersect = set(expected_names).intersection(set([row.name for row in c]))
        # Check if the expected_years line up with the archive entries years.
        assert len(intersect) == len(expected_names)
