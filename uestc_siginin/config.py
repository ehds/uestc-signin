import os
import logging
import json
logging.basicConfig(filename='./logs/uestc.log', level=logging.INFO)


class UserConfig(object):
    def __init__(self, config_path):
        self._config_path = config_path
        self.parse()

    def parse(self):
        if not os.path.exists(self._config_path):
            error_message = "There is not config file {}".format(
                self._config_path)
            logging.error(error_message)
            raise ValueError(error_message)
        data = {}
        with open(self._config_path, 'r') as f:
            data = json.load(f)
        assert "user" in data and "password" in data
        self.user = data["user"]
        self.passwd = data["password"]
