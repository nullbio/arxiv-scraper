import abc
import os

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class AbstractModelMeta(abc.ABCMeta, type(models.Model)):
    pass


class AbstractModel(models.Model, metaclass=AbstractModelMeta):
    class Meta:
        abstract = True


class Plugin(AbstractModel):
    name = models.TextField(unique=True)
    enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    # TODO: Add __str__ methods for all models, which is the human readable object output
    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Document(AbstractModel):
    title = models.TextField()
    categories = models.ManyToManyField(Category)
    page_link = models.TextField(unique=True, null=True, blank=True)
    file_link = models.TextField(unique=True, null=True, blank=True)
    # Flag to skip downloading the html page. This should be set to true if
    # the plugin does not intend on downloading the file.
    skip_page_download = models.BooleanField(default=False)
    # Flag to skip downloading the target document file.
    # This should be set to true if the plugin does not intend on downloading the file.
    skip_file_download = models.BooleanField(default=False)
    download_failed = models.BooleanField(default=False)
    download_attempt_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        abstract = True


class Paper(Document):
    paper_id = models.TextField(unique=True)
    authors = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    doi = models.TextField(unique=True, null=True, blank=True)
    related_doi = models.TextField(null=True, blank=True)
    issn = models.TextField(null=True, blank=True)
    report_no = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    journal_ref = models.TextField(null=True, blank=True)
    # the date the paper was published (v0 of the paper)
    published_date = models.DateTimeField(null=True, blank=True)
    # the publish date of the latest new version of the paper (if any)
    updated_date = models.DateTimeField(null=True, blank=True)
    withdrawn = models.BooleanField(default=False)

    class Meta:
        abstract = True

    # @abc.abstractmethod
    # def must_implement(self):
    #    """
    #    This method must be implemented by any subclass of AbstractModel.
    #    """
    #    pass


class File(AbstractModel):
    md5_hash = models.TextField(max_length=32, unique=True)
    name = models.TextField(unique=True)
    # Generic foreign key fields, for any document type.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    # if we want to prune old papers we don't care about on our disk,
    # but still keep a record of the file in the database,
    # we can prune them and record the date they were deleted.
    # this way we don't have stale links to non-existent files in our database.
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)


# delete the file from disk if it exists
@receiver(pre_delete, sender=File, dispatch_uid="filePreDelete")
async def handlePreDelete(sender, **kwargs):
    file = kwargs["instance"]
    filepath = os.path.join(settings.DOWNLOAD_DIRECTORY, file.name)
    if os.path.isfile(filepath):
        os.remove(filepath)


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
