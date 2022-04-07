import logging
from abc import abstractmethod

import redis

from config import REDIS_SERVER, TEST_ID

__author__ = "Antongiacomo Polimeno"
__email__ = "antongiacomo.polimeno@moon-cloud.eu"


class StopChecker:

    # True must stop, False must continue
    def __init__(self):
        super().__init__()

    @abstractmethod
    def check_stop(self):
        pass


class RedisStopChecker(StopChecker):
    def __init__(self):
        super().__init__()
        self.notified = False

    def check_stop(self):
        try:
            r = redis.StrictRedis(host=REDIS_SERVER, port=6379, db=0)
            row = int(r.get(TEST_ID))
            return row == 1
        except redis.exceptions.ConnectionError:
            if not self.notified:
                logging.warning("Controls kill database not reachable")
                self.notified = True
            return False
        except ValueError:
            logging.critical("String in the Redis value")
        except Exception as e:
            print(e)
        return True
