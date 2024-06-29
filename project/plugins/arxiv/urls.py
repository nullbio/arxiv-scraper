from django.urls import path

from project.plugins.arxiv import views

app_name = "arxiv"

urlpatterns = [
    path("", views.index, name="index"),
    # path("<int:pk>/", views.DetailView.as_view(), name="plugin_detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="plugin_results"),
]
