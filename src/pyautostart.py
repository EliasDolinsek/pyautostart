import getpass
import os
import plistlib
from abc import ABC, abstractmethod


class Autostart(ABC):

    @abstractmethod
    def enable(self, name: str, options: dict = None):
        pass

    @abstractmethod
    def disable(self, name: str):
        pass


class MacAutostart(Autostart):

    def __init__(self, base_path=f"/Users/{getpass.getuser()}/Library/LaunchAgents"):
        self.base_path = base_path

    def enable(self, name: str, options: dict = None):
        if options is None:
            raise ValueError("options must not be None")
        if "Label" not in options:
            raise ValueError("'Label' must be specified in options")
        if "ProgramArguments" not in options:
            raise ValueError("'ProgramArguments' must be specified in options")

        with open(self.get_path_for_name(name), "wb") as file:
            plistlib.dump(options, file)

    def disable(self, name: str):
        path = self.get_path_for_name(name)
        if os.path.exists(path):
            os.remove(path)
        else:
            raise FileNotFoundError(f"Could not find file {path}")

    def get_path_for_name(self, name):
        return f"{self.base_path}/{name}.plist"
