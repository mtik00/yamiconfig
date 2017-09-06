#!/usr/bin/env python
# coding: utf-8
'''
Yet another configuration object!
'''

# Imports #####################################################################
from __future__ import print_function
import os
import sys
import copy
import collections
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

from .schema import Schema, SchemaError


# Metadata ####################################################################
__author__ = 'Timothy McFadden'
__creationDate__ = '06-SEPT-2017'
__license__ = 'MIT'
__version__ = '0.2.0'


# This header will be written to the user config file during
# ``Config.store_defaults``.
USER_CONFIG_HEADER = (
    '# This file contains the settings available for the user to override.  Simply'
    '# un-comment the setting (defaults are shown), and restart the application.\n'
)


(IS_WIN, IS_LIN, IS_MAC) = (
    'win' in sys.platform,
    'lin' in sys.platform,
    'darwin' in sys.platform)


# The configuration class
class Configuration(collections.MutableMapping):
    '''YAML-based configuration settings'''
    def __init__(
        self, default_config_file=None, default_yaml_text=None,
        user_config_files=None, valid_schema=None, ignore_extra_keys=False,
        use_os_keys=False
    ):
        self.default_file = default_config_file
        self.user_files = user_config_files or []

        if not (default_config_file or default_yaml_text):
            raise ValueError("Must use either `default_config_file` or `default_yaml_text`")

        if default_config_file:
            with open(default_config_file) as fh:
                self._default_raw = fh.read()
        else:
            self._default_raw = default_yaml_text

        if valid_schema:
            self.schema = Schema(valid_schema, ignore_extra_keys=ignore_extra_keys)
        else:
            self.schema = None

        self.use_os_keys = use_os_keys
        self.extra_data = {}  # Settings not sure in a config file

        self.load_configs()

    def __delitem__(self):
        pass

    def __getitem__(self, key):
        value = self.extra_data[key] if (key in self.extra_data) else self._calculated[key]
        return self._decode_os_value(value)

    def __iter__(self):
        return iter(self._calculated + self.extra_data)

    def __len__(self):
        return len(self._calculated + self.extra_data)

    def __setitem__(self, key, value):
        if key in self._default:
            self._calculated[key] = value
        else:
            self.extra_data[key] = value

    def _decode_os_value(self, value):
        '''Return the value of a dictionary based on its keys'''
        if not (self.use_os_keys and isinstance(value, dict)):
            return value

        # If the value keys consist only of 'windows', 'linux', and 'mac'
        os_keys = ['windows', 'linux', 'mac']
        if not [v_key for v_key in value.keys() if v_key not in os_keys]:
            if IS_WIN:
                return value['windows']
            elif IS_MAC:
                return value['mac']
            else:
                return value['linux']

        return value

    def _validate(self, yaml_data):
        '''
        Make sure the types of the data are the same types as the default.
        '''
        if self.schema:
            self.schema.validate(yaml_data)

    def reset(self, path=None):
        '''
        Resets all configuration settings to the default, ignoring any current
        user settings.

        :param str path: The path to the configuration file to write, if any
        '''
        self._calculated = copy.deepcopy(self._default)
        self.extra_data.clear()

        if path:
            self.store_config(path)

    def load_configs(self):
        '''Find all of the config files and load them in'''
        self._default = self.loads(self._default_raw)
        self._calculated = copy.deepcopy(self._default)

        for fpath in self.user_files:
            temp = self.load_file(fpath)
            if temp:
                self._calculated.update(temp)

    def load_file(self, path):
        '''Load and validate a file, and return the data.'''
        if os.path.isfile(path):
            with open(path) as fh:
                text = fh.read()

            data = YAML().load(text) or {}

            try:
                self._validate(data)
            except SchemaError:
                print("ERROR: Configuration file [%s] did not validate" % path)
                raise

            return data

        return None

    def loads(self, yaml_string):
        '''Load a configuration from a string'''
        data = YAML().load(yaml_string) or {}

        try:
            self._validate(data)
        except SchemaError:
            raise

        return data

    def dump(self, obj=None):
        '''
        Return the *calculated* configuration as a YAML-formatted string.

        NOTE: This only includes keys that are part of the default config.
        '''
        obj = obj or self._calculated
        d = StringIO()
        YAML().dump(obj, d)
        return d.getvalue()

    def is_default(self, key):
        '''Returns True if the key has not been modified from the default'''
        return bool(
            (key in self._calculated) and
            (key in self._default) and
            (self._calculated[key] == self._default[key])
        )

    def store_config(self, fpath):
        '''Stores the current configuration to the YAML file'''
        with open(fpath, 'wb') as fh:
            fh.write(self.dump())

    def store_defaults(self, fpath):
        '''Creates a new file with all default settings commented out'''
        default_text_lines = open(self.default_file).readlines()
        new_lines = [USER_CONFIG_HEADER]

        # Comment out all of the lines
        for line in default_text_lines:
            line = line.strip()
            if line and (not line.startswith('#')):
                line = "# " + line
            new_lines.append(line)

        with open(fpath, 'wb') as fh:
            fh.write('\n'.join(new_lines))
