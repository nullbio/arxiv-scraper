import logging
import os

from django.apps import AppConfig
from django.core.checks import Error, register


class CoreConfig(AppConfig):
    name = "project.core"

    def ready(self):
        self.log = logging.getLogger(__name__)

        if os.environ.get("RUN_MAIN") == "true":
            # Import signals to register them
            from project.core import signals  # noqa: F401
            from project.core.plugins import plugin_manager

            self.log.debug("Initializing core app and plugins")

            plugin_manager.initialize_plugins()


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
