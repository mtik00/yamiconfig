#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name, unused-import, protected-access
"""
Test setting values in the config.
"""

from pytest import raises

from . import config, strict_config


def test_default(config):
    """Default strict is set to False"""
    config.set("a.b.c.d", 4)
    assert config.get("a.b.c.d") == 4


def test_strict_config(strict_config):
    """Strict default should raise an exception"""
    with raises(KeyError):
        strict_config.set("test.asdf", 42)


def test_force_strict(config):
    """Using .get(strict=True) w/ default False should raise an exception"""
    with raises(KeyError):
        config.set("test.asdf", 99, strict=True)


def test_force_unstrict(strict_config):
    """Using .get(strict=False) w/ default Strict config should not raise an exception"""
    strict_config.set("test.a.b.c.d", 1E6, strict=False)
