import sys
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

class Yaml(YAML):

    def dump_all(self, data, stream=None, *args, **kwargs):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump_all(self, data, stream, *args, **kwargs)
        if inefficient:
            return stream.getvalue()
