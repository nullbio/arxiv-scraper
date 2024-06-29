from datetime import datetime

from django.db import models

import project.core.models as core_models

# TODO: Add __str__ methods for all models, which is the human readable object output


class Archive(models.Model):
    category = models.ForeignKey(core_models.Category, on_delete=models.CASCADE)
    # The oldest year the archive has papers for
    end_year = models.IntegerField()

    def __str__(self):
        return f"{self.category.name} ({self.end_year} - {datetime.now().year})"


class MonthlyArchiveManager(models.Manager):
    def finished_scraping(self):
        return self.filter(
            total_entries__gt=0, scraped_entries__gte=models.F("total_entries")
        ).values_list("pk", flat=True)


# the monthly archive urls for a given category, for example:
# https://arxiv.org/list/<category_name>/<yyyy-mm>
# each monthly archive page has a total number of entries that we can scrape
# by paginating through the pages.
class MonthlyArchive(models.Model):
    category = models.ForeignKey(core_models.Category, on_delete=models.CASCADE)
    year = models.TextField(
        max_length=4,
    )
    month = models.TextField(
        max_length=2,
    )
    total_entries = models.IntegerField()
    # number of entries that have had their paper metadata scraped
    # (but NOT pdf downloaded, and NOT extra_metadata scraped)
    scraped_entries = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        constraints = [
            # should only ever be one monthly archive for a given category
            models.UniqueConstraint(
                fields=["category", "year", "month"],
                name="unique_monthly_archive_mismatch",
            )
        ]

    objects: MonthlyArchiveManager = MonthlyArchiveManager()

    def __str__(self):
        return f"{self.category.name} ({self.month}/{self.year})"


# used by the integrity scanner to record discrepancies in the scraped data.
# The integrity scanner needs to be run separately from the scraper.
#
# during an integrity check scrape, if we notice that the total entries
# have changed over time, we record it here so it can be further investigated.
class TotalEntriesMismatch(models.Model):
    monthly_archive = models.ForeignKey(MonthlyArchive, on_delete=models.CASCADE)
    # the total entries at date of mismatch scan (created_at)
    total_entries = models.IntegerField()
    # the countried entries at date of mismatch scan (created_at)
    counted_entries = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["monthly_archive", "total_entries", "counted_entries"],
                name="unique_total_entries_mismatch",
            )
        ]


# this is the data scraped from the individual monthly archive urls, for ex:
# https://arxiv.org/list/cs/<yyyy-mm>
class Paper(core_models.Paper):
    monthly_archive = models.ForeignKey(MonthlyArchive, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
