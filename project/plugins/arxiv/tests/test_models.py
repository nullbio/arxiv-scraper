import pytest

from project.core.models import Category
from project.plugins.arxiv.models import Archive, MonthlyArchive


class TestModels:

    @pytest.fixture(autouse=True)
    def reload_model_fixtures(self, reload_model_fixtures):
        # Reload the model fixtures after every test
        pass

    @pytest.mark.django_db
    def test_archive_fixtures(self):
        a = Archive.objects.all()
        # Should be 11 arxiv categories, so therefore 11 archive entries
        assert len(a) == 11

        expected_years = [0]
        years = [row.end_year for row in a]

        assert len(years) == 11, f"Expected 11 results, found {len(years)}"

        expected_years = [
            1992,
            1996,
            1993,
            1996,
            1992,
            1993,
            2003,
            2008,
            2017,
            2017,
            2017,
        ]

        for i in range(len(years)):
            assert (
                years[i] == expected_years[i]
            ), f"Expected {expected_years[i]} results: {years[i]}"
            return

    @pytest.mark.django_db
    def test_get_finished_monthly_archive_urls(self):
        assert not len(MonthlyArchive.objects.finished_scraping())

        ma = MonthlyArchive(
            category=Category.objects.get(name="cs"),
            year="2015",
            month="01",
            total_entries=5,
            scraped_entries=0,
        )
        ma.save()
        assert not len(MonthlyArchive.objects.finished_scraping())

        ma.scraped_entries = 2
        ma.save()
        assert not len(MonthlyArchive.objects.finished_scraping())

        ma.scraped_entries = 5
        ma.save()
        assert len(MonthlyArchive.objects.finished_scraping()) == 1
