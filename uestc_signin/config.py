import os
import logging
import json
import configparser
logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = 'uestc.conf'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(object, metaclass=Singleton):
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self._config_path = config_path
        self.parse()

    def parse(self):
        if not os.path.exists(self._config_path):
            raise ValueError(f"{self._config_path} not exists")
        self.cf = configparser.ConfigParser()
        self.cf.read(self._config_path)

    def __getattr__(self, attr):
        return self.cf[self._section][attr]


class UserConfig(Config):
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self._section = "user"
        super(UserConfig, self).__init__(config_path)


class MailConfig(Config):
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        super(MailConfig, self).__init__(config_path)
        self._section = "mail"


if __name__ == "__main__":
    m = MailConfig("../uestc.conf")
    print(m.pop_host)
    c = UserConfig("../uestc.conf")
    print(c.password)
