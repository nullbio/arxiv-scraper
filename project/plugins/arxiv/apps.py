import logging

from django.apps import AppConfig
from django.core.checks import Error, register


class ArxivConfig(AppConfig):
    name = "project.plugins.arxiv"
    label = "arxiv"
    verbose_name = "Arxiv Plugin"

    def ready(self):
        self.log = logging.getLogger(__name__)

        # set up the scraper
        pass


@register()
def database_check(app_configs, **kwargs):
    from project.plugins.arxiv.models import Archive

    errors = []
    if Archive.objects.all().count() == 0:
        errors.append(
            Error(
                "Database fixtures not loaded.",
                hint='Run the "manage.py loaddata **/fixtures/*.json" command.',
                id="scrapii.plugins.arxiv.E001",
            )
        )
    return errors
