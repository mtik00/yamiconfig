#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import config


def test_default(config):
    assert len(config._configs) == 2
    assert config.get("test.bool") == True


def test_web_override(config):
    """web.root should have been overridden"""
    assert config.get("web.root") == "/var/www/html"
