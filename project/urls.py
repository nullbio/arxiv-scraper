"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import logging
from importlib import import_module

from django.contrib import admin
from django.urls import include, path

from project.core.models import Plugin

app_name = "core"

logger = logging.getLogger(__name__)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("project.core.urls")),
]


# Dynamically load plugin URLs
def dynamic_plugin_urls():
    urlpatterns = []
    try:
        plugins = Plugin.objects.all()
        for plugin in plugins:
            module_path = plugin.module_path + ".urls"
            try:
                imported_module = import_module(module_path)
                urlpatterns.append(
                    path(
                        f"{plugin.name.lower()}/",
                        include(
                            (imported_module, plugin.name.lower()),
                            namespace=plugin.name.lower(),
                        ),
                    )
                )
            except ModuleNotFoundError:
                logger.error(
                    f"Cannot load module urls, module not found: {module_path}"
                )
    except Exception as e:
        logger.error(f"Cannot load plugins, database not configured: {e}")
        return urlpatterns
    return urlpatterns


# Add plugin URLs to the main URLs
urlpatterns += dynamic_plugin_urls()
