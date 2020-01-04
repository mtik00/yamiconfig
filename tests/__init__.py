#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pytest setup.
"""
import pytest
import ruamel.yaml

import yamiconfig

DEFAULT = """
---

test:
  path: /opt/var/etc/usr/bin/t
  list:
    - 0
    - 1
    - 2
  bool: true
  vars: "one, two, three"

web:
  root: /var/www/html/public
"""

USER = """
---

test:
  user: tim

web:
  root: /var/www/html
"""


@pytest.fixture
def config(monkeypatch):
    """A Config fixture with `strict=False`"""

    # We need our own loader so we can use our own YAML text.
    def mock_load(path: str):
        if path.endswith("config.yaml"):
            return yamiconfig.ConfigItem(
                data=yamiconfig.string_to_yaml(DEFAULT), path=path
            )
        return yamiconfig.ConfigItem(data=yamiconfig.string_to_yaml(USER), path=path)

    monkeypatch.setattr(yamiconfig, "load_yaml_file", mock_load)

    app_config = yamiconfig.Config("pytest-app", user_dirs=["/pytest"], default_strict=False)

    return app_config


@pytest.fixture
def strict_config(monkeypatch):
    """A Config fixture with `strict=True`"""

    # We need our own loader so we can use our own YAML text.
    def mock_load(path: str):
        if path.endswith("config.yaml"):
            return yamiconfig.ConfigItem(
                data=yamiconfig.string_to_yaml(DEFAULT), path=path
            )
        return yamiconfig.ConfigItem(data=yamiconfig.string_to_yaml(USER), path=path)

    monkeypatch.setattr(yamiconfig, "load_yaml_file", mock_load)

    app_config = yamiconfig.Config("pytest-app", user_dirs=["/pytest"], default_strict=True)

    return app_config
