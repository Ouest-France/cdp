#!/usr/bin/env python2.7

import ConfigParser, StringIO

class PropertiesParser(ConfigParser.ConfigParser, object):

    def read(self, filename):
        try:
            text = open(filename).read()
        except IOError:
            pass
        else:
            file = StringIO.StringIO("[shell]\n" + text)
            self.readfp(file, filename)

    def get(self, prop):
        return super(PropertiesParser, self).get("shell", prop)
