from abc import ABC, abstractmethod


class Autostart(ABC):
    def __init__(self, options: dict):
        self.options = options

    @abstractmethod
    def enable(self, name, username=None, **kwargs):
        pass

    @abstractmethod
    def disable(self, name, username=None):
        pass
