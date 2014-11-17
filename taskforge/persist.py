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

    def task_update(self, task):
        self._task.task_update(task)
