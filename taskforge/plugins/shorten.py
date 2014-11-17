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


class Shortener(PluginBase):
    _base = 'http://da.gd/'
    max_length = 24 # default longest non-shortened URL

    def __init__(self, **kwargs):
        self.max_length = kwargs.get('max_length',
                                     self.max_length)

        super(Shortener, self).__init__(**kwargs)

    def pre_run(self):
        pass

    def post_run(self):
        pass

    def _shorten_contents(self, text):
        """Returns a list of URLs in order of appearance

        Will not return if:
          - URL is already shortened
          - URL is shorter than it would be shortened
        """
        urls = [
            m[0] for m in _URL_REGEX.findall(text)
            if len(m[0]) > self.max_length and not m[0].startswith(self._base)
        ]

        for url in urls:
            if re.match('.*{}\.\.\..*'.format(url), text):
                continue
            shortened = self._shorten_url(url)
            self.log.debug("Shortened {} to {}".format(url, shortened))
            text = text.replace(url, shortened)

        return text

    def _shorten_url(self, url):
        r = requests.get(self._base + 's',
                         params={'url': url})
        if r.status_code != 200:
            return None
        return r.text.strip()

    def _shorten_urls(self, desc, annotations):
        """Given arbitrary text, shorten any url-like segments"""
        for index in range(len(annotations)):
            annotations[index] = self._shorten_contents(annotations[index])
        desc = self._shorten_contents(desc)
        return desc, annotations

    def process_task(self, task):
        newDesc, anno = self._shorten_urls(str(task['description']), list(task['annotations']))
        results = task.update({
                'description': newDesc,
                'annotations': anno,
            })
        if any(results.values()):
            return task
        return None
