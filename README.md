# pyautostart

PyAutostart is a Python library for making all sorts of executables files be run after the user logged in into his
computer for macOS, Linux and Windows.

Please note that Linux is not yet being supported.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyAutostart.

```bash
pip install pyautostart
```

## Usage

### Platform independent

#### Make a file be run after login

The `options` dict must contain `args` which has to be a list that usually contains the path to the executable file.
The `name` parameter of `autostart.enable` sets the name of the file which will then be created by the platform
dependent implementation.

```python
from pyautostart import SmartAutostart

autostart = SmartAutostart()
options = {
    "args": [
        "/path/to/executable/file"
    ]
}
autostart.enable(name="com.example.myapplication", options=options)
```

#### Disable automatic execution

Calling `autostart.disable` will delete the file which is being created by `autostart.enable`. The `name` parameter has
to be the one set during `autostart.enable`.

````python
from pyautostart import SmartAutostart

autostart = SmartAutostart()
autostart.disable(name="com.example.myapplication")
````

### macOS

#### Make a file be run after login

The `options` dict contains the configuration for launchd. For a list of all valid options and their meanings, go to
the [Wikipedia article of launchd](en.wikipedia.org/wiki/Launchd/). The `name` parameter of `autostart.enable` sets the
name of the file which will be stored in `/Users/<username>/Library/LaunchAgents` if not changed.

```python
from pyautostart import MacAutostart

autostart = MacAutostart()
options = {
    "Label": "Name of",
    "ProgramArguments": [
        "python3",
        "/path/to/your/file.py"
    ]
}
autostart.enable(name="com.example.myapplication", options=options)
```

#### Disable automatic execution

Calling `autostart.disable` will delete the file which is being created by `autostart.enable`. The `name` parameter has
to be the one set during `autostart.enable`.

````python
from pyautostart import MacAutostart

autostart = MacAutostart()
autostart.disable(name="com.example.myapplication")
````

### Windows

#### Make a file be run after login

The `options` dict must contain `executable`, which has to store to path to your executable file. `autostart.enable`
will then create a `.bat` file which by default contains `start "" <executable>"`.

This file will be stored
inside `C:\\Users\\<username>\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup`.

If you want to replace the `start ""` command. Add `command: "<command>"` to the options dict.

```python
from pyautostart import WindowsAutostart

autostart = WindowsAutostart()
options = {
    "executable": "C:\\path\\to\\your\\executable",
}
autostart.enable(name="com.example.myapplication", options=options)
```

#### Disable automatic execution

Calling `autostart.disable` will delete the file which is being created by `autostart.enable`. The `name` parameter has
to be the one set during `autostart.enable`.

````python
from pyautostart import WindowsAutostart

autostart = WindowsAutostart()
autostart.disable(name="com.example.myapplication")
````

### Linux

Linux is not supported yet.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU GENERAL PUBLIC LICENSE](https://choosealicense.com/licenses/gpl-3.0/)
