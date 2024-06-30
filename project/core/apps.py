import _thread
import logging
import os
import threading
import time

from django.apps import AppConfig, apps
from django.core.checks import Error, register

import project.settings as settings


class CoreConfig(AppConfig):
    name = "project.core"

    def ready(self):
        self.log = logging.getLogger(__name__)

        # Prevent the autoreload runserver from running this code,
        # Otherwise it will be run twice.
        if os.environ.get("RUN_MAIN") == "true":
            # Wait for all apps/plugins to be ready
            while not apps.check_apps_ready():
                self.log.debug("Waiting for all apps to be ready...")
                time.sleep(1)

            from project.core.models import Plugin
            from project.core.plugins import PluginManager

            self.log.debug("Initializing core app and plugins")

            # set up the plugin manager
            self.plugin_manager = PluginManager(Plugin.objects.all())

            # run the plugins
            for plugin_classname, plugin_path in settings.AVAILABLE_PLUGINS:
                self.plugin_manager.load_plugin(plugin_classname, plugin_path)

            self.plugin_manager.run_all_plugins()


@register()
def database_check(app_configs, **kwargs):
    from project.core.models import Category, Plugin

    errors = []
    check_failed = False
    try:
        if Plugin.objects.all().count() == 0:
            check_failed = True

        if Category.objects.all().count() == 0:
            check_failed = True
    except Exception as e:
        errors.append(
            Error(
                f"Database not initialized: {e}",
                hint="Create the database using the manage.py migrate command.",
                id="scrapii.core.E001",
            )
        )

    if check_failed:
        errors.append(
            Error(
                "Database fixtures not loaded.",
                hint='Run the "manage.py loaddata **/fixtures/*.json" command.',
                id="scrapii.core.E002",
            )
        )
    return errors
