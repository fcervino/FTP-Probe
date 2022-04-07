import json
from abc import ABCMeta

from Writer import AbstractWriter


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbcSingleton(Singleton, ABCMeta):
    pass


class EvidenceWriter(AbstractWriter, metaclass=AbcSingleton):
    def __init__(self, indent=2, prettify=True):
        super().__init__()
        self.indent = indent
        self.prettify = prettify

    def prettifier(self, param):
        if self.prettify:
            return json.dumps(param, indent=self.indent)
        else:
            return param

    def store_result(self, status, extra_data, retention_policy=None):
        tup = {"status": status, "data": extra_data}
        print(self.prettifier((tup)))
