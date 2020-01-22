#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name, unused-import, protected-access
"""
Tests for the `has_path` function
"""

from . import config
from yamiconfig import has_path


def test_default(config):
    """Test default config YAML"""
    # assert has_path("web.root", config)
    # assert not has_path("asdf.zxcv", config)
    assert has_path("test.null_item", config)
