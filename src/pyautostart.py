import getpass
import os
import platform
import plistlib
from abc import ABC, abstractmethod


class Autostart(ABC):

    def __init__(self):
        """Abstract autostart class."""
        pass

    @abstractmethod
    def enable(self, name: str, options: dict = None):
        """
        Call this method if you want to add a file to the automatic boot.
        :param name: desired name for autostart file without file ending (e.g. com.example.myapplication).
        :param options: contains platform dependent information like the path to the executable file.
        """
        pass

    @abstractmethod
    def disable(self, name: str):
        """
        Call this method if you want to remove a file from automatic boot.
        :param name: name of autostart file without file ending.
        """
        pass

    @abstractmethod
    def is_enabled(self, name):
        """
        Returns weather a autostart file with a specific name exists.
        :param name: name of autostart file without file ending.
        :return: True if autostart with file exists, False if not.
        """
        pass


class SmartAutostart(Autostart):
    """Platform independent implementation."""

    def __init__(self):
        if platform.system() == "Darwin":
            self.autostart = MacAutostart()
        elif platform.system() == "Windows":
            self.autostart = WindowsAutostart()
        else:
            raise SystemError("Not supported system")

    def enable(self, name: str, options: dict = None):
        if self.autostart is MacAutostart:
            parsed_options = {
                "Label": name,
                "ProgramArguments": options["args"]
            }
        elif self.autostart is WindowsAutostart:
            parsed_options = {
                "executable": "".join(options["args"])
            }
        else:
            raise SystemError("Not supported system")

        return self.enable(name, parsed_options)

    def disable(self, name: str):
        return self.autostart.disable(name)

    def is_enabled(self, name):
        return self.autostart.is_enabled(name)


class MacAutostart(Autostart):

    def __init__(self, base_path=f"/Users/{getpass.getuser()}/Library/LaunchAgents"):
        """Implementation for macOS."""
        self.base_path = base_path

    def enable(self, name: str, options: dict = None):
        """
        Enables autostart for a file on macOS.
        :param name: name of plist file which is being stored in base_path.
        :param options: requires "Label" (name of the job) and "ProgramArguments" (array of strings representing a
        UNIX command). For more options and information go to https://en.wikipedia.org/wiki/Launchd.
        """
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

    def is_enabled(self, name):
        return os.path.exists(self.get_path_for_name(name))

    def get_path_for_name(self, name):
        return f"{self.base_path}/{name}.plist"


class WindowsAutostart(Autostart):

    def __init__(self):
        """Implementation for windows."""
        pass

    def enable(self, name: str, options: dict = None):
        """
        Enables autostart for a file on windows.
        :param name: name of the executable file without file ending which is being stored in
        C:\\Users\\<username>\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup.
        :param options: requires "executable" (path to file which should be executed). "command" can be specified
        optionally to change the leading command (default='start ""').
        """
        if options is None:
            raise ValueError("Options must not be None")
        if "executable" not in options:
            raise ValueError("'executable' must be specified in options")

        if "command" not in options:
            command = 'start ""'
        else:
            command = options["command"]

        with open(self.get_path_for_name(name), "w") as file:
            executable = options["executable"]
            file.write(f'{command} {executable}')

    def disable(self, name: str):
        path = self.get_path_for_name(name)
        if os.path.exists(path):
            os.remove(path)
        else:
            raise FileNotFoundError(f"Could not find file {path}")

    def is_enabled(self, name):
        return os.path.exists(self.get_path_for_name(name))

    @staticmethod
    def get_path_for_name(name):
        return f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Microsoft\\" \
               f"Windows\\Start Menu\\Programs\\Startup\\{name}.bat"
