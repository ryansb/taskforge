import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class Forge(App):
    log = logging.getLogger(__name__)

    def __init__(self):
        self.log.debug("Heyo")
        super(Forge, self).__init__(
            description='Task Forge',
            version='0.1',
            command_manager=CommandManager('taskforge.commands'),
        )

    def initialize_app(self, argv):
        self.log.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def cli():
    print "hello"
    app = Forge()
    app.run(sys.argv[1:])