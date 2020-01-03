#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "0.1.0"


import os
from functools import partial

import ruamel.yaml


# Other search dirs to find overrides
USER_DIRS = ["./instance"]


class Config:
    def __init__(self, app_name: str, defaults: str = "---", init: bool = False):
        default_folder = os.path.expanduser(f"~/.config/{app_name}")
        default_file = os.path.join(default_folder, "config.yaml")

        if init:
            if not os.path.exists(default_folder):
                os.makedirs(default_folder)

            with open(default_file, "w") as fh:
                fh.write(defaults)

        with open(default_file) as fh:
            data =  fh.read()

        self._config = ruamel.yaml.load(data, ruamel.yaml.RoundTripLoader) or {}

        if not isinstance(self._config, dict):
            raise TypeError("This object only support dict configs")

    def get(self, path: str, strict: bool = False):
        """
        Get a setting from the dotted path.

        :param bool strict: Raise an exception if the path is not found.
        """
        method = "__getitem__" if strict else "get"
        steps = path.split('.')

        result = getattr(self._config, method)(steps[0])
        if not result:
            return result

        for step in steps[1:]:
            result = getattr(result, method)(step)
            if not result:
                return result

        return result


def main():
    c = Config("yamiconfig-test", init=False)
    print(c.get('test.bool', strict=True))


if __name__ == "__main__":
    main()
