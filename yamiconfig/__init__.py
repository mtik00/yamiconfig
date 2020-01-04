#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "0.3.0"


import os
from dataclasses import dataclass
from functools import partial
from typing import List

import ruamel.yaml

DEBUG = False


@dataclass
class ConfigItem:
    path: str
    data: dict


def string_to_yaml(string_data):
    return ruamel.yaml.load(string_data, ruamel.yaml.RoundTripLoader) or {}


def load_yaml_file(path: str):
    """Loads a YAML file and returns a ConfigItem if the path exists, None otherwise."""
    if not os.path.isfile(path):
        if DEBUG:
            print(f"WARNING: '{path}' not found")

        return None

    with open(path) as fh:
        yaml_data = fh.read()

    return ConfigItem(
            path=path,
            data=string_to_yaml(yaml_data)
        )


class Config:
    def __init__(
        self,
        app_name: str,
        default_strict: bool = False,
        user_dirs: List[str] = ["./instance"],
    ):
        self.app_name = app_name
        self.default_strict = default_strict
        self.user_dirs = user_dirs
        self.default_folder = os.path.expanduser(f"~/.config/{app_name}")
        self.default_file = os.path.join(self.default_folder, "config.yaml")
        self.reload()

    def __str__(self):
        return f"<Config app_name: {self.app_name}>"

    def init(self, default_yaml: str = "---"):
        """Writes the initial YAML file to the default location"""
        if not os.path.exists(self.default_folder):
            os.makedirs(self.default_folder)

        with open(self.default_file, "w") as fh:
            fh.write(default_yaml or "---")

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

    def get(self, path: str, strict: bool = None):
        """
        Get a setting from the dotted path.

        :param bool strict: Raise an exception if the path is not found.
        """
        strict = strict if strict is not None else self.default_strict
        missing_key = False
        for config in self._configs:
            val = None
            try:
                val = self._get(path, config.data, strict)
            except KeyError:
                missing_key = True

            if val:
                if DEBUG:
                    print(f"setting '{path}' found in: {config.path}")
                return val

        if missing_key:
            raise KeyError(f"Setting not found: {path}")

    def _get(self, path: str, config: dict, strict: bool = False):
        """
        Get a setting from the dotted path in the

        :param bool strict: Raise an exception if the path is not found.
        """
        method = "__getitem__" if strict else "get"
        steps = path.split(".")

        result = getattr(config, method)(steps[0])
        if not result:
            return result

        for step in steps[1:]:
            result = getattr(result, method)(step)
            if not result:
                return result

        return result


if __name__ == "__main__":
    # DEBUG = True
    c = Config("yamiconfig-test", default_strict=True)
    print(c.get("webx", strict=False))
