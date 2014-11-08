#!/bin/env python
# -*- coding: utf8 -*-

import os
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
            nickname:
                type: string
            options:
                type: object
            weight:
                type: number
"""


def load_config(conf_path=''):
    if not conf_path:
        conf_path = os.path.join(
            os.path.expandvars('$HOME'),
            '.taskforgerc')
    with open(conf_path, 'r') as fh:
        config = yaml.load(fh)

    validate(config, yaml.load(_config_schema))

    return config
