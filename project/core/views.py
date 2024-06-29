from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import get_resolver, reverse
from django.views import generic

from project.core.models import Plugin


def index(request):
    plugins = Plugin.objects.all()
    # TODO: show scraping status against each plugin
    context = {
        "plugins_list": plugins,
    }
    return render(request, "core/index.html", context)


def plugin_toggle(request, pk):
    plugin = get_object_or_404(Plugin, pk=pk)
    plugin.enabled = not plugin.enabled
    plugin.save()
    return HttpResponseRedirect(reverse("core:index"))


class DetailView(generic.DetailView):
    model = Plugin
    template_name = "core/plugins/detail.html"


class ResultsView(generic.DetailView):
    model = Plugin
    template_name = "core/plugins/results.html"
