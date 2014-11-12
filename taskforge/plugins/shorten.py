#!/bin/env python
# -*- coding: utf8 -*-

from functools import lru_cache
import re

import requests

from taskforge.plugin import PluginBase


class Shortener(PluginBase):
    _base = 'http://da.gd/s'

    def __init__(self, **kwargs):
        super(Shortener, self).__init__(**kwargs)

    def pre_run(self):
        pass

    def post_run(self):
        pass

    @lru_cache(255)
    def _shorten_url(self, url):
        return requests.get(self._base,
                            params={'url': url}
                            ).text.strip()

    def _shorten_urls(self, text):
        """Given arbitrary text, shorten any url-like segments"""
        pass

    def _is_shortened(self, url):
        return bool(re.match('^http://da.gd/.*$', url))

    def process_task(self, task):
        pass
