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

import re

import requests

from taskforge.plugin import PluginBase

"""Adapted from https;//gist.github.com/uogbuji/705383"""
_URL_REGEX = re.compile(
    ur'(?i)\b((?:https?://)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+'
    ur'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?'
    ur'\xab\xbb\u201c\u201d\u2018\u2019]))')


class Bugwarrior(PluginBase):
    def __init__(self, **kwargs):
        super(Bugwarrior, self).__init__(**kwargs)

    def pre_run(self):
        from subprocess import call
        ret = call(["bugwarrior-pull"])
        if ret == 0:
            print "Bugwarrior run successfully."
        else:
            print "Bugwarrior failed with exit code {}".format(ret)

    def post_run(self):
        pass

    def process_task(self, task):
        pass
