#!/usr/bin/env python
class Context(object):

    def __init__(self):
        self._login=""

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, v):
        self._login = v
