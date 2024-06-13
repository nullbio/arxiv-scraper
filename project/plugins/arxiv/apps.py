import logging

from django.apps import AppConfig


class ArxivConfig(AppConfig):
    name = "project.plugins.arxiv"
    label = "arxiv"
    verbose_name = "Arxiv Plugin"

    def ready(self):
        self.log = logging.getLogger(__name__)

        # set up the scraper
        pass
