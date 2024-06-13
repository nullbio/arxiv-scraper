import logging
import os

from django.apps import AppConfig

import project.settings as settings
from project.core.plugins import PluginManager


class CoreConfig(AppConfig):
    name = "project.core"

    def ready(self):
        self.log = logging.getLogger(__name__)

        # Prevent the autoreload runserver from running this code,
        # Otherwise it will be run twice.
        if os.environ.get("RUN_MAIN") == "true":
            self.log.debug("Initializing core app")

            # set up the plugin manager
            self.plugin_manager = PluginManager()

            # run the plugins
            for plugin_classname, plugin_path in settings.AVAILABLE_PLUGINS:
                self.plugin_manager.load_plugin(plugin_classname, plugin_path)

            self.plugin_manager.run_all_plugins()


"""
TODO:
@register
def example_check(app_configs, **kwargs):
    # hooks for django checks, to ensure the app is configured correctly
    # field, model, database and manager checks done differently though. See docs.
    # see: https://docs.djangoproject.com/en/5.0/topics/checks/

"""
