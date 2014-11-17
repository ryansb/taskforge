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
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff.complete import CompleteCommand


class Forge(App):
    log = logging.getLogger(__name__)

    def __init__(self):
        self.log.debug("Heyo")
        super(Forge, self).__init__(
            description='Task Forge',
            version='0.1',
            command_manager=CommandManager('taskforge.commands'),
        )
        self.command_manager.add_command('complete', CompleteCommand)

    def initialize_app(self, argv):
        self.log.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def cli():
    app = Forge()
    app.run(sys.argv[1:])
