# coding=utf-8
#
# Copyright (c) 2020 The UESTC-Signin Authors. All rights reserved.
# Use of this source code is governed by a MIT-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
# Authors: ehds(ds.he@foxmail.com)

import sys
import os
import threading
from uestc_signin.logging import create_logger
from uestc_signin.config import UserConfig, MailConfig, DEFAULT_CONFIG_PATH

from uestc_signin.task import MainTask

# from uestc_signin.task import MainTask
# TODO use argpase

logger = create_logger(__name__)
log_dir = "logs"
data_dir = "data"

def init_dir():
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

def main():
    if len(sys.argv) > 1:
        config_dir = sys.argv[1]
    confs = os.listdir(config_dir)
    if len(confs) == 0:
        logger.warning("There is no conf to run")
        return

    try:
        init_dir()
    except OSError as e:
        logger.warning(f"Can't init log and data dir error {e}")
    # get user config
    threads = []
    for conf in confs:
        conf_path = os.path.join(config_dir,conf)
        user_config = UserConfig(conf_path)
        mail_config = MailConfig(conf_path)
        print(user_config.user)
        threads.append(threading.Thread(target=MainTask,args=(user_config,mail_config)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()