from django.urls import path

from project.core import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("plugin/toggle/<int:pk>/", views.plugin_toggle, name="plugin_toggle"),
]
