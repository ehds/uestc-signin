# coding=utf-8
#
# Copyright (c) 2020 The UESTC-Signin Authors. All rights reserved.
# Use of this source code is governed by a MIT-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
# Authors: ehds(ds.he@foxmail.com)

import os
import logging
import json
import configparser
logger = logging.getLogger(__name__)

CONF_DIR = "confs"
LOGS_DIR = "logs"
DATA_DIR = "data"

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(object, metaclass=Singleton):
    def __init__(self, config_path):
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
    def __init__(self, config_path):
        self._section = "user"
        super(UserConfig, self).__init__(config_path)


class MailConfig(Config):
    def __init__(self, config_path):
        super(MailConfig, self).__init__(config_path)
        self._section = "mail"
