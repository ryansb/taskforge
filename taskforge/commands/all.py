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

import logging

from cliff.command import Command

from taskforge.config import Configurable
from taskforge.plugin import load_plugin, run_plugin


class RunAll(Command, Configurable):
    """A command that runs a single taskforge plugin.

    If the plugin is disabled in your .taskforgerc that will be overridden"""

    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(RunAll, self).__init__(app, app_args)

    def get_parser(self, prog_name):
        parser = super(RunAll, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("%s" % self.config)
        for conf in self.config['plugins']:
            if not conf.get('enabled', False):
                self.log.debug("Skipping disabled plugin %s" % conf['name'])
                continue

            self.log.debug("loading \"{name} = {entrypoint}\"".format(
                **conf))

            plugin = load_plugin(conf)

            run_plugin(plugin)
        self.log.info("Done running plugins.")
