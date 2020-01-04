#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from . import config, strict_config

from pytest import raises


def test_default(config):
    """Default strict is set to False"""
    config.get("test.asdf")


def test_strict_config(strict_config):
    """Strict default should raise an exception"""
    with raises(KeyError):
        strict_config.get("test.asdf")


def test_force_strict(config):
    """Using .get(strict=True) w/ default False should raise an exception"""
    with raises(KeyError):
        config.get("test.asdf", strict=True)


def test_force_unstrict(strict_config):
    """Using .get(strict=False) w/ default Strict config should not raise an exception"""
    strict_config.get("test.asdf", strict=False)
