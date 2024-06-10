from abc import ABC, abstractmethod


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
