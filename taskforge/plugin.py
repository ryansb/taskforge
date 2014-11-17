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

import abc
import logging
import pkg_resources
import six

import lockfile

from persist import Warrior


LOCK_PATH = '/tmp/taskforge'


@six.add_metaclass(abc.ABCMeta)
class PluginBase(object):
    log = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        # TODO: do something with option parameters
        pass

    @abc.abstractmethod
    def pre_run(self):
        """Optional pre-run setup. Only run once."""
        pass

    @abc.abstractmethod
    def post_run(self):
        """Optional post-run teardown"""
        pass

    @abc.abstractmethod
    def process_task(self, task):
        """Receive a single taskw.task:Task object and returns the task after
        processing.

        If there are no changes, None should be returned
        """
        raise NotImplementedError


class DummyPlugin(PluginBase):
    def __init__(self, *args, **kwargs):
        super(DummyPlugin, self).__init__(*args, **kwargs)
        self.opts = kwargs

    def pre_run(self):
        self.log.debug("prerun for DummyPlugin")

    def post_run(self):
        self.log.debug("postrun for DummyPlugin")

    def process_task(self, task):
        self.log.debug("Dummy plugin loaded with options: "
                      "{}".format(self.opts))
        self.log.info("Task pro:{} tags:{} found".format(task['project'], task['tags']))
        for a in task['annotations']:
            self.log.info(a[:80])
        return None


def load_plugin(plugin_conf):
    """Takes a full plugin configuration dict

    Returns an instance of the plugin loaded and initialized with the plugin
    options
    """
    ep = pkg_resources.EntryPoint.parse(
        "{name} = {entrypoint}".format(**plugin_conf),
        pkg_resources.get_distribution(plugin_conf.get('module', 'taskforge'))
    )

    return ep.load()(**plugin_conf.get('options', {}))

@lockfile.locked(LOCK_PATH)
def run_plugin(loaded):
    """Takes a plugin and runs it over pending/waiting tasks
    """
    warrior = Warrior()
    loaded.pre_run()
    for t in warrior.iter_tasks():
        orig_desc = str(t['description'])
        m = loaded.process_task(t)
        if m is not None:
            warrior.task_update(m)
            loaded.log.info("Updated task {id} with new description/annotations".format(**t))
            loaded.log.debug("Task {id} desc={description}".format(**t))
    loaded.post_run()
