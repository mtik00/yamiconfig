#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name, unused-import, protected-access
"""
Tests for user overrides.
"""

from . import config


def test_default(config):
    """Test default config YAML"""
    assert len(config._configs) == 3
    assert config.get("test.bool")


def test_web_override(config):
    """web.root should have been overridden"""
    assert config.get("web.root") == "/var/www/html"
