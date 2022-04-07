from abc import abstractmethod, ABCMeta

__author__ = "Antongiacomo Polimeno"
__email__ = "antongiacomo.polimeno@moon-cloud.eu"


class AbstractWriter(metaclass=ABCMeta):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def store_result(self, status, extra_data, retention_policy=None):
        pass
