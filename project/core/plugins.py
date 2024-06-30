import logging
from abc import ABC, abstractmethod

from celery import shared_task
from celery.contrib.abortable import AbortableAsyncResult, AbortableTask
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver


class PluginManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.plugins = {}
        self.tasks = {}

    def register_plugin(self, app_label, plugin_class):
        self.plugins[app_label] = plugin_class()

    def start_plugin(self, app_label):
        if app_label in self.plugins:
            plugin = self.plugins[app_label]
            task = plugin.run.delay()
            self.tasks[app_label] = task

    def stop_plugin(self, app_label):
        if app_label in self.tasks:
            task = self.tasks[app_label]
            AbortableAsyncResult(task.id).abort()
            del self.tasks[app_label]

    def initialize_plugins(self):
        from project.core.models import Plugin

        for plugin in Plugin.objects.filter(enabled=True):
            app_label = plugin.module_path.split(".")[-1]
            if app_label in self.plugins:
                self.start_plugin(app_label)


class BasePlugin(ABC):
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
    def task(self):
        pass

    @shared_task(bind=True, base=AbortableTask)
    def run(self):
        while not self.is_aborted():
            self.task()


plugin_manager = PluginManager()
