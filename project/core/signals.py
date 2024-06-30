import logging
import os

from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from project.core.models import File, Plugin
from project.core.plugins import plugin_manager


# delete the file from disk if it exists
@receiver(pre_delete, sender=File, dispatch_uid="filePreDelete")
async def handlePreDelete(sender, **kwargs):
    file = kwargs["instance"]
    filepath = os.path.join(settings.DOWNLOAD_DIRECTORY, file.name)
    if os.path.isfile(filepath):
        os.remove(filepath)


# When a plugin is enabled or disabled, start or stop the plugin
@receiver(post_save, sender=Plugin)
def handle_plugin_change(sender, instance, **kwargs):
    log = logging.getLogger(__name__)
    app_label = instance.module_path.split(".")[-1]
    if instance.enabled:
        log.debug(f"Starting plugin: {app_label}")
        plugin_manager.start_plugin(app_label)
    else:
        log.debug(f"Stopping plugin: {app_label}")
        plugin_manager.stop_plugin(app_label)
