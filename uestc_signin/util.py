# coding=utf-8
#
# Copyright (c) 2020 The UESTC-Signin Authors. All rights reserved.
# Use of this source code is governed by a MIT-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
# Authors: ehds(ds.he@foxmail.com)

import time


def get_date_str():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
