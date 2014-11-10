#!/bin/env python
# -*- coding: utf8 -*-

import os
import copy
import yaml
from jsonschema import validate

_config_schema = """
type: object
properties:
    logging:
        properties:
            level:
                type: string
            file:
                type: string
    plugins:
        type: array
        properties:
            enabled:
                type: boolean
            name:
                type: string
            entrypoint:
                type: string
            options:
                type: object
            weight:
                type: number
"""


class Configurable(object):
    _conf = None

    @property
    def config(self):
        if not self._conf:
            self._conf = self._load_config()
        return copy.deepcopy(self._conf)

    def _load_config(self, conf_path=''):
        if not conf_path:
            conf_path = os.path.join(
                os.path.expandvars('$HOME'),
                '.taskforgerc')
            conf_path = os.path.join(
                '/home/ryansb/code/taskforge/',
                'config_sample.yml')
        with open(conf_path, 'r') as fh:
            config = yaml.load(fh)

        validate(config, yaml.load(_config_schema))

        return config
