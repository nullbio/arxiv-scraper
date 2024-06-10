from project.core.plugin import PluginBase


class Arxiv(PluginBase):
    def __init__(self):
        self._name = "Arxiv"
        self._version = "0.0.1"
        self._description = "Arxiv scraper and deleted paper monitor"

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def description(self):
        return self._description

    def run(self):
        pass
