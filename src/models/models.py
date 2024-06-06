import os

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Category(models.Model):
    name = models.TextField(unique=True)
    # The oldest year the archive has papers for
    end_year = models.IntegerField()
    # Whether we don't want to scrape this category anymore
    disabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)


class MonthlyArchive(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    year = models.TextField(
        max_length=4,
    )
    month = models.TextField(
        max_length=2,
    )
    total_entries = models.IntegerField()
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


# used by the integrity scanner to record discrepancies in the scraped data.
# The integrity scanner needs to be run separately from the scraper.
class TotalEntriesMismatch(models.Model):
    monthly_archive = models.ForeignKey(
        MonthlyArchive, on_delete=models.CASCADE
    )
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


class Paper(models.Model):
    monthly_archive = models.ForeignKey(
        MonthlyArchive, on_delete=models.CASCADE
    )
    arxiv_id = models.TextField(unique=True)
    title = models.TextField()
    authors = models.TextField()
    comment = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    journal_ref = models.TextField(null=True, blank=True)
    pdf_link = models.TextField(unique=True)
    page_link = models.TextField(unique=True)
    withdrawn = models.BooleanField()
    # we can skip downloading the paper by setting this to True
    skip_download = models.BooleanField(default=False)
    download_failed = models.BooleanField(default=False)
    download_attempt_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)


class PDF(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    file_md5_hash = models.TextField(max_length=32, unique=True)
    file_name = models.TextField(unique=True)
    # if we want to prune old papers we don't care about on our disk,
    # but still keep a record of the file in the database,
    # we can prune them and record the date they were deleted.
    # this way we don't have stale links to non-existent files in our database.
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)


# delete the file from disk if it exists
@receiver(pre_delete, sender=PDF, dispatch_uid="pdfPreDelete")
async def handlePreDelete(sender, **kwargs):
    pdf = kwargs["instance"]
    filepath = os.path.join(settings.DOWNLOAD_DIRECTORY, pdf.file_name)
    if os.path.isfile(filepath):
        os.remove(filepath)


# We separate this because the archive scrape doesn't contain these fields.
# If we want these, it must be done using the API or scraping the paper page.
class ExtraMetadata(Paper):
    summary = models.TextField()
    doi = models.TextField(null=True, blank=True)
    related_doi = models.TextField(null=True, blank=True)
    report_no = models.TextField(null=True, blank=True)
    # the date the paper was published (v0 of the paper)
    published_date = models.DateTimeField()
    # the publish date of the latest new version of the paper (if any)
    updated_date = models.DateTimeField(null=True, blank=True)
