import logging
import time

from celery import shared_task
from django.apps import AppConfig
from django.core.checks import Error, Warning, register

from project.core.plugins import BasePlugin


class ArxivPlugin(BasePlugin):
    def __init__(self):
        self._name = "Arxiv"
        self._version = "0.0.1"
        self._description = "Arxiv scraper and deleted paper monitor"
        self._config = {}
        self.log = logging.getLogger(__name__)

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def description(self):
        return self._description

    def setup(self, config):
        return self._config

    @shared_task(bind=True)
    def task(self):
        self.log.debug("Arxiv plugin task running")
        time.sleep(1)
        # Your Arxiv-specific code here


class ArxivConfig(AppConfig):
    name = "project.plugins.arxiv"
    label = "arxiv"
    verbose_name = "Arxiv Plugin"

    def ready(self):
        from project.core.plugins import plugin_manager

        log = logging.getLogger(__name__)

        log.debug("Registering Arxiv plugin")
        plugin_manager.register_plugin("arxiv", ArxivPlugin)


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


@register()
def check_arxiv_plugin(app_configs, **kwargs):
    from project.core.plugins import plugin_manager

    if "arxiv" not in plugin_manager.plugins:
        return [
            Warning(
                "Arxiv plugin is not registered",
                hint="Ensure ArxivConfig.ready() method is called and registers the plugin.",
                id="scrapii.plugins.arxiv.W001",
            )
        ]
    return []
