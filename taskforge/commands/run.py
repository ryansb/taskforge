#!/bin/env python
# -*- coding: utf8 -*-

import logging

from cliff.command import Command

from taskforge.config import Configurable
from taskforge.plugin import load_plugin


class Run(Command, Configurable):
    """A command that runs a single taskforge plugin.

    If the plugin is disabled in your .taskforgerc that will be overridden"""

    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(Run, self).__init__(app, app_args)

    def get_parser(self, prog_name):
        parser = super(Run, self).get_parser(prog_name)
        parser.add_argument(
            "name",
            metavar="<name>",
            help="Name of the plugin",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("%s" % self.config)

        plugin_conf = filter(lambda x: x['name'] == parsed_args.name,
                             self.config['plugins'])
        if not plugin_conf:
            self.log.warn("Plugin {} not found.".format(parsed_args.name))
            return 1

        plugin_conf = plugin_conf[0]

        self.log.debug("loading \"{name} = {entrypoint}\"".format(
            **plugin_conf))

        solo = load_plugin(plugin_conf)

        solo.pre_run()
        for t in []:
            solo.process_task(None)
        solo.post_run()
