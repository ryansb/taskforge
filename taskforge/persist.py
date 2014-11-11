#!/bin/env python
# -*- coding: utf8 -*-

import os

import taskw

class Warrior(object):
    _task = None
    def __init__(self, taskrc=''):
        if not taskrc:
            taskrc = os.path.join(
                os.path.expandvars('$HOME'),
                '.taskrc')
        if self._task is None:
            self._task = taskw.TaskWarrior(config_filename=taskrc,
                                           marshal=True)

    def iter_tasks(self):
        return self._task.filter_tasks({
            'or': [
                ('status', 'pending'),
                ('status', 'waiting'),
            ]
        })

    def update_task(self, task):
        self._task.update_task(task)
