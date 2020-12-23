import os
import plistlib
import unittest
from cgitb import Hook
from unittest.mock import patch, MagicMock

from src.pyautostart import MacAutostart


class TestMacAutostart(unittest.TestCase):

    def test_get_path_for_name(self):
        autostart = MacAutostart()
        result = autostart.get_path_for_name("name")
        self.assertEquals("/System/Library/LaunchAgents/name.plist", result)

    def test_enable_missing_name(self):
        autostart = MacAutostart()
        self.assertRaises(TypeError, autostart.enable)

    def test_enable_options_none(self):
        autostart = MacAutostart()
        self.assertRaises(ValueError, autostart.enable, "name")

    def test_enable_options_missing_label(self):
        autostart = MacAutostart()
        self.assertRaises(ValueError, autostart.enable, "name", {"ProgramArguments": "args"})

    def test_enable_options_missing_program_arguments(self):
        autostart = MacAutostart()
        self.assertRaises(ValueError, autostart.enable, "name", {"Label": "label"})

    def test_enable(self):
        autostart = MacAutostart()
        plistlib.dump = MagicMock()
        options = {"Label": "label", "ProgramArguments": "args"}

        with patch("builtins.open", unittest.mock.mock_open()) as m:
            autostart.enable("name", options)

        m.assert_called_once_with("/System/Library/LaunchAgents/name.plist", "wb")
        plistlib.dump.assert_called_once_with(options, m())

    def test_disable(self):
        autostart = MacAutostart()
        autostart.get_path_for_name = MagicMock(return_value="/path/to/file")

        os.path.exists = MagicMock(return_value=True)
        with patch("os.remove") as remove:
            autostart.disable("name")

        remove.assert_called_once_with("/path/to/file")
        autostart.get_path_for_name.assert_called_once_with("name")

