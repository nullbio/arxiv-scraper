from django.apps import AppConfig


class ArxivConfig(AppConfig):
    name = "plugins.arxiv"
    verbose_name = "Arxiv Plugin"

    def ready(self):
        # set up the scraper
