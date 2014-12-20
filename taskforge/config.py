# -*- coding: utf8 -*-
"""
Copyright 2014 Ryan Brown <sb@ryansb.com>

This file is part of taskforge.

taskforge is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

taskforge is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with taskforge.  If not, see <http://www.gnu.org/licenses/>.
"""

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
            module:
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
        with open(conf_path, 'r') as fh:
            config = yaml.load(fh)

        validate(config, yaml.load(_config_schema))

        return config
