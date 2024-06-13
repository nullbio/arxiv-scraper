import importlib
import logging
from abc import ABC, abstractmethod


class PluginManager:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.active_plugins = []
        self.config = {}

    def load_plugin(self, class_name, module_name):
        """Create an instance of the given plugin, and add it to the
        PluginManager's active plugins list.

        Args:
            class_name (str): The name of the plugin class (e.g. "Arxiv")
            module_name (str): The path to the module (e.g. "project.plugins.arxiv")
        """
        if class_name not in self.active_plugins:
            module = importlib.import_module(f"{module_name}.plugin")
            plugin = getattr(module, class_name)()
            self.active_plugins.append(plugin)

    def run_all_plugins(self):
        self.log.debug("Running all active plugins")
        for plugin in self.active_plugins:
            plugin.setup(self.config)
            plugin.run()


class PluginBase(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def version(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def setup(self, config):
        pass

    @abstractmethod
    def run(self):
        pass
