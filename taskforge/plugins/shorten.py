#!/bin/env python
# -*- coding: utf8 -*-

import re

import requests

from taskforge.plugin import PluginBase

"""Adapted from https;//gist.github.com/uogbuji/705383"""
_URL_REGEX = re.compile(
    ur'(?i)\b((?:https?://)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+'
    + ur'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?'
    + ur'\xab\xbb\u201c\u201d\u2018\u2019]))')


class Shortener(PluginBase):
    _base = 'http://da.gd/s'

    def __init__(self, **kwargs):
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
            if len(m[0]) >= 24 and not m[0].startswith('http://da.gd/')
        ]

        for url in urls:
            if re.match('.*{}\.\.\..*'.format(url), text):
                continue
            shortened = self._shorten_url(url)
            self.log.debug("Shortened {} to {}".format(url, shortened))
            text = text.replace(url, shortened)

        return text

    def _shorten_url(self, url):
        r = requests.get(self._base,
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
