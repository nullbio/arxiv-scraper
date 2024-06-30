import abc

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AbstractModelMeta(abc.ABCMeta, type(models.Model)):
    pass


class AbstractModel(models.Model, metaclass=AbstractModelMeta):
    class Meta:
        abstract = True


class Plugin(AbstractModel):
    # The user-facing name of the plugin, e.g. "Arxiv" or "Arxiv Scraper"
    name = models.TextField(unique=True)
    # The path to the plugin module, e.g. "project.plugins.arxiv"
    module_path = models.TextField(unique=True)
    enabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    # TODO: Add __str__ methods for all models, which is human readable object output
    def __str__(self):
        return self.name


# The arxiv categories, for example: math, cs, etc.
# This table is seeded on database creation.
# All plugins should conform to the arXiv category naming conventions.
class Category(AbstractModel):
    # Names must conform to the arXiv category naming conventions for all plugins.
    name = models.TextField(unique=True)

    # Scraping can be disabled for a category globally by setting this to True.
    disabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return self.name


class Document(AbstractModel):
    title = models.TextField()
    categories = models.ManyToManyField(Category)
    # if the user has favorited this document, it can be easily found
    favorite = models.BooleanField(default=False)
    # rating is a number between 0 and 5
    rating = models.FloatField(default=0)
    # an additional flag that can be used by plugins for misc purposes
    # is usually a number between 0 and 5, but can technically be anything
    # as it is not depended on by the core application.
    flag = models.FloatField(default=0)
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


# class Video(Document): // TODO: if we want to support video downloading/scraping
# class Image(Document): // TODO: if we want to support images


class File(AbstractModel):
    md5_hash = models.TextField(max_length=32, unique=True)
    name = models.TextField(unique=True)
    # Generic foreign key fields, for any document type.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    # if we want to prune old documents we don't care about on our disk,
    # we can prune them and record the date they were deleted.
    # this way we don't have stale links to non-existent files in our database.
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
