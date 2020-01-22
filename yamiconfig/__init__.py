#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module holds the interface for the Config object.

This object is used for interacting with the application configuration.
"""
__version__ = "0.3.0"


import os
from dataclasses import dataclass
from functools import partial
from typing import Any, Dict, List, Optional, Union

import ruamel.yaml

DEBUG = False


@dataclass
class ConfigItem:
    """A dataclass to describe a configuration stored in a file"""

    path: str
    data: dict

    def get(self, path: str) -> Any:
        """
        Get a setting from the dotted path.

        Raises `KeyError` if any part of the path is not found.

        :param bool strict: Raise an exception if the path is not found.
        """
        return get_setting(path, self.data, strict=True)


def string_to_yaml(string_data: str) -> Union[Any, Dict[Any, Any]]:
    """Converts a YAML string to a Python data structure"""
    return ruamel.yaml.load(string_data, ruamel.yaml.RoundTripLoader) or {}


def load_yaml_file(path: str) -> Optional[ConfigItem]:
    """Loads a YAML file and returns a ConfigItem if the path exists, None otherwise."""
    if not os.path.isfile(path):
        if DEBUG:
            print(f"WARNING: '{path}' not found")

        return None

    with open(path) as file_object:
        yaml_data = file_object.read()

    return ConfigItem(path=path, data=string_to_yaml(yaml_data))


def get_setting(path: str, config: dict, strict: bool = False):
    """
    Get a setting from the dotted path in the dictionary.

    :param bool strict: Raise an exception if the path is not found.
    """
    method = "__getitem__" if strict else "get"
    steps = path.split(".")

    # Do we have the _raw_ path, like {'a.b.c.d': 4}?
    try:
        return config[path]
    except KeyError:
        pass

    result = getattr(config, method)(steps[0])
    if not result:
        return result

    for step in steps[1:]:
        result = getattr(result, method)(step)
        if not result:
            return result

    return result


def initialize_settings_file_from_yaml(
    app_name: str, default_yaml: str, force: bool = False
) -> None:
    """
    Initializes a new YAML settings file for the application.
    """
    Config(app_name=app_name).init(default_yaml=default_yaml, force=force)


def initialize_settings_file_from_file(
    app_name: str, path: str, force: bool = False
) -> None:
    """
    Initializes a new YAML settings file for the application.
    """
    with open(path) as stream:
        default_yaml = stream.read()

    Config(app_name=app_name).init(default_yaml=default_yaml, force=force)


class Config:
    """
    This class can be used to interact with an application configuration.

    The configuration files should be stored as YAML files.  The default folder
    to look for is `~/.config/{app_name}`.

    NOTE: You should call `init` before attempting to use the configuration.
    """

    def __init__(
        self,
        app_name: str,
        default_strict: bool = False,
        default_folder: str = None,
        user_dirs: List[str] = None,
    ):
        self.app_name = app_name
        self.default_strict = default_strict
        self.user_dirs = user_dirs if user_dirs is not None else ["./instance"]
        self.default_folder = (
            default_folder
            if default_folder is not None
            else os.path.expanduser(f"~/.config/{app_name}")
        )
        self.default_file = os.path.join(self.default_folder, "config.yaml")
        self.reload()

    def __str__(self):
        return f"<Config app_name: {self.app_name}>"

    def init(self, default_yaml: str = "---", force: bool = False):
        """Writes the initial YAML file to the default location.

        :param str default_yaml: The default YAML string to store
        :param bool force: Force re-creating the config.
        """
        if os.path.exists(self.default_folder) and (not force):
            raise Exception(f"Config folder {self.default_folder} already exists!")

        if not os.path.exists(self.default_folder):
            os.makedirs(self.default_folder)

        with open(self.default_file, "w") as file_object:
            file_object.write(default_yaml or "---")

    def reload(self):
        """Reloads the configuration from the file system."""
        self._default_config = load_yaml_file(self.default_file)
        self._configs = [self._default_config]

        for user_dir in reversed(self.user_dirs):
            config_file = os.path.join(user_dir, f"{self.app_name}.yaml")
            self._configs.append(load_yaml_file(config_file))

        # This stores the list of configurations in reverse order.  The first
        # element is the "most" important and the last element is the "least"
        # important.
        self._configs = [x for x in reversed(self._configs) if x]

        if DEBUG and (not self._configs):
            print("WARNING: No config files found")

        # Finally, add an override config to store dynamic settings.
        self._configs = [ConfigItem(path="override", data={})] + self._configs

    def get(self, path: str, strict: bool = None) -> Any:
        """
        Get a setting from the dotted path.

        :param bool strict: Raise an exception if the path is not found.
        """
        strict = strict if strict is not None else self.default_strict

        for config in self._configs:
            try:
                val = config.get(path)
                missing_key = False
            except KeyError:
                missing_key = True

            if (not missing_key) and (val is not None):
                if DEBUG:
                    print(f"setting '{path}' found in: {config.path}")
                return val

        if missing_key and strict:
            raise KeyError(f"Path not found: '{path}'")

        return None

    def set(
        self, path: str, value: Any, strict: bool = None, persist: bool = False
    ) -> None:
        """
        Sets a value at the specified path.

        There's no real benefit of dealing with the complexity of nested
        structures.  Just use the raw path to set the value in the
        override config.
        """
        strict = strict if strict is not None else self.default_strict

        # If we're strict, raise an Exception if we don't already have
        # this setting in our config.
        if strict:
            self.get(path, strict=True)

        self._configs[0].data[path] = value

        if persist:
            yaml = ruamel.yaml.YAML()
            default_config = self._configs[-1]
            default_config.data[path] = value
            with open(default_config.path, "w") as stream:
                yaml.dump(default_config.data, stream)


if __name__ == "__main__":
    app_config = Config(  # pylint: disable=invalid-name
        "yamiconfig-test", default_strict=True
    )
    print(app_config.get("webx", strict=False))
