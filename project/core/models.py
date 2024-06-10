import abc
import os

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class AbstractModelMeta(abc.ABCMeta, type(models.Model)):
    pass


class AbstractModel(models.Model, metaclass=AbstractModelMeta):
    class Meta:
        abstract = True


# The arxiv categories, for example: math, cs, etc.
# This table is seeded on database creation.
#
# by default, all categories are scraped. Set DISABLED_CATEGORIES environment
# variable to a comma-separated list of category names to disable scraping.
class Category(AbstractModel):
    # Names must conform to the arXiv category naming conventions for all plugins.
    name = models.TextField(unique=True)

    # Scraping can be disabled for a category by setting this to True.
    # This will override the ENABLED_CATEGORIES environment variable,
    # and the default behavior of scraping all categories.
    disable_override = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)


# this is the data scraped from the individual monthly archive urls, for ex:
# https://arxiv.org/list/cs/<yyyy-mm>
class Paper(AbstractModel):
    title = models.TextField()
    authors = models.TextField()
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


# We separate these additional paper metadata fields because the archive
# scrape doesn't contain these fields. If we want these, it must be done
# using the API or scraping the paper page.
class ExtraMetadata(Paper):
    summary = models.TextField()
    doi = models.TextField(null=True, blank=True)
    related_doi = models.TextField(null=True, blank=True)
    report_no = models.TextField(null=True, blank=True)
    # the date the paper was published (v0 of the paper)
    published_date = models.DateTimeField()
    # the publish date of the latest new version of the paper (if any)
    updated_date = models.DateTimeField(null=True, blank=True)


# insert the categories we want to scrape and the oldest year they have papers for
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('cond-mat', 1992);
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('math-ph', 1996);
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('nlin', 1993);
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('physics', 1996);
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('math', 1992);
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('cs', 1993);
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('q-bio', 2003);
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('q-fin', 2008);
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('stat', 2017);
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('eess', 2017);
# INSERT OR IGNORE INTO category (name, end_year) VALUES ('econ', 2017);
