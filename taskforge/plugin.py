#!/bin/env python
# -*- coding: utf8 -*-

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
        m = loaded.process_task(t)
        if m is not None:
            warrior.task_update(m)
    loaded.post_run()
