# coding=utf-8
#
# Copyright (c) 2020 The UESTC-Signin Authors. All rights reserved.
# Use of this source code is governed by a MIT-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
# Authors: ehds(ds.he@foxmail.com)

from uestc_signin.logging import create_logger
import requests
import json
import datetime
import random
import time
import threading
from enum import Enum
from abc import abstractmethod
from .config import DATA_DIR
from .util import get_date_str
from .uestc_login import Login, relogin
from .notify import Notify
import os
logger = create_logger(__name__)


class Task(object):

    class RequestMethod(Enum):
        GET = 1
        POST = 2

    def __init__(self, config):
        self.method = Task.RequestMethod.GET
        self.cookies = {}
        self.url = ''
        self.data = {}
        self.interval = 24  # hour
        self.last_run = 0
        self.config = config

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def runable(self):
        pass

    @abstractmethod
    def init_data(self):
        pass

    def _get_server_date(self):
        url = "https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/api/base/getServerDate.do"
        res = requests.post(url, cookies=self.cookies)
        if res.status_code == requests.codes.ok:
            return res.text
        else:
            return ""


class TemperatureTask(Task):
    def __init__(self, config):
        """TemperatureTask"""
        super(TemperatureTask, self).__init__(config)
        self.url = 'https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/tempReport/T_REPORT_TEMPERATURE_YJS_SAVE.do'
        self.method = self.RequestMethod.POST
        self._data_path = os.path.join(
            DATA_DIR, f"{self.config.user}_user.json")
        self.last_run = []
        self.init_data()
        self.headers = {}

    def init_data(self):
        """ init cookies and user data """
        self.cookies = Login.load_cookies(self.config.user)
        logger.info(self.cookies)
        user_info_url = "https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/api/base/getUserDetailDB.do"
        res = requests.post(user_info_url, cookies=self.cookies).content.decode(
            encoding="utf-8")
        user_info = json.loads(res)
        assert "data" in user_info, "get userinfo failed"
        with open(self._data_path, "w") as f:
            json.dump(user_info["data"], f)

        self.headers = {
            'Origin': 'https://eportal.uestc.edu.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
        }

    def _is_need_to_run(self, index):
        server_date = self._get_server_date()
        post_data = {
            "pageNumber": 1,
            "pageSize": "10",
            "USER_ID": self.config.user,
            "KSRQ": server_date,
            "JSRQ": server_date,
        }
        url = "https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/tempReport/getMyTempReportDatas.do"
        res = requests.post(url, data=post_data, cookies=self.cookies)
        data = json.loads(res.content)
        TempData = data["datas"]["getMyTempReportDatas"]
        if TempData["totalSize"] == 0:
            return True
        else:
            if len(list(filter(lambda x: x["DAY_TIME"] == str(index), TempData["rows"]))) < 1:
                return True
        return False

    def _get_tem_post_data(self, index):
        # fucking names，why client need to post
        assert index >= 1 and index <= 3, "index must be 1,2 or 3"
        display_names = ["早上", "中午", "晚上"]
        # data from user info
        user_info_keys = ["USER_ID", "USER_NAME", "DEPT_CODE", "DEPT_NAME"]
        data = {}
        with open(self._data_path, 'r') as f:
            user = json.load(f)
            for key in user_info_keys:
                data[key] = user[key]

        # data we need to set various every day
        cur_date_str, time_str = get_date_str().split(" ")
        data['CREATED_AT'] = f'{cur_date_str} {time_str[:-3]}'
        data['NEED_DATE'] = cur_date_str
        data['DAY_TIME'] = str(index)
        data['DAY_TIME_DISPLAY'] = display_names[index-1]
        # !!! be careful, temperature must in [36.3,36.7]
        data['TEMPERATURE'] = "%.1f" % (random.uniform(36.3, 36.7))
        data['WID'] = ""
        return data

    def run(self):
        """ 一次性打完所有温度 """
        # TODO 按时打卡

        post_url = self.url
        # morning:1、noon:2、night:3
        for i in range(1, 4):
            if not self._is_need_to_run(i):
                continue
            post_data = self._get_tem_post_data(i)
            res = requests.post(post_url, data=post_data,
                                cookies=self.cookies, headers=self.headers)
            logger.info("TEMPERATURE Task data：{}, RESULT: {}".format(post_data,
                                                                      res.content.decode(encoding="utf-8")))
            # TODO  need to retry if fail

    def runable(self):
        # 判断上次打卡时间
        pass


class StuReportTask(Task):
    def __init__(self, config):
        super(StuReportTask, self).__init__(config)
        self.url = 'https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/dailyReport/T_REPORT_EPIDEMIC_CHECKIN_YJS_SAVE.do'
        self.method = self.RequestMethod.POST
        self.last_run = 0
        self._data_path = os.path.join(
            DATA_DIR, f"{self.config.user}_report.json")
        self.cookies = {}
        self.init_data()

    def init_data(self):
        self.cookies = Login.load_cookies(self.config.user)
        lastest_daily_report_url = "https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/dailyReport/getLatestDailyReportData.do"
        post_data = {
            "pageNum": 1,
            "pageSize": 10,
            "USER_ID": self.config.user
        }
        headers = {
            'Origin': 'https://eportal.uestc.edu.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
        }
        last_daily_data = requests.post(
            lastest_daily_report_url, data=post_data, headers=headers, cookies=self.cookies).content
        logger.info(last_daily_data)
        data = json.loads(last_daily_data)

        data = data["datas"]["getLatestDailyReportData"]["rows"][0]
        with open(self._data_path, 'w') as f:
            json.dump(data, f)

    def _is_need_to_run(self):
        server_date = self._get_server_date()
        post_data = {
            "pageNumber": 1,
            "pageSize": "10",
            "USER_ID": self.config.user,
            "KSRQ": server_date,
            "JSRQ": server_date,
        }
        url = "https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/dailyReport/getMyDailyReportDatas.do"
        res = requests.post(url, data=post_data, cookies=self.cookies)
        data = json.loads(res.content)
        if(data["datas"]["getMyDailyReportDatas"]["totalSize"] > 0):
            return False
        return True

    def _get_post_data(self):
        data = {}
        with open(self._data_path, 'r') as f:
            data = json.load(f)
        # Normally we not need to change report data, just post lastest data
        cur_date_str, time_str = get_date_str().split(" ")
        data['CZRQ'] = cur_date_str+" 00:00:00"
        data['NEED_CHECKIN_DATE'] = cur_date_str
        data['CREATED_AT'] = get_date_str()
        #wid = self._get_today_wid()
        data['WID'] = ""
        return data

    def _get_today_wid(self):
        self.cookies = Login.load_cookies(self.config.user)
        url = "https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/mobile/dailyReport/getMyTodayReportWid.do"
        post_data = {
            "pageNum": "1",
            "pageSize": "10",
            "USER_ID": self.config.user,
        }
        res = requests.post(url, data=post_data, cookies=self.cookies).content
        data = json.loads(res)
        wid = data["datas"]["getMyTodayReportWid"]["rows"][0]["WID"]
        return wid

    def run(self):
        if not self._is_need_to_run():
            # the task have completed
            return

        post_url = self.url
        data = self._get_post_data()
        headers = {
            'Origin': 'https://eportal.uestc.edu.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',

        }
        res = requests.post(post_url, data=data,
                            cookies=self.cookies, headers=headers)
        logger.info("STUREPORT Task data：{}, RESULT: {}".format(data,
                                                                res.content.decode(encoding="utf-8")))

    def runable(self):
        now = time.time()


class UESTCPunch(object):
    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd
        login = Login(self.user, self.passwd)

    def start(self):
        timer = threading.Timer(5, self.run, [], {})
        timer.start()

    def run(self):
        pass


class MyThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(10):
            pass
            # call a function


def data_compare(date_1, date_2):
    # date: %Y-%m-%d
    a = datetime.datetime.strptime(date_1, "%Y-%m-%d")
    b = datetime.datetime.strptime(date_2, "%Y-%m-%d")
    return a < b


def main_task(user_config, mail_config):
    logger = create_logger(__name__, user_config.user)
    last_check_day = "1970-01-01"
    subject = "UESTC-Notify"
    today_fail_count = 0
    while True:

        current_date = datetime.datetime.now()
        current_date_str = current_date.strftime("%Y-%m-%d")

        # if today not run task and hour is greater 8am and try count < 10
        if data_compare(last_check_day, current_date_str) and current_date.hour > 8:
            try:
                if relogin(user_config):
                    logger.info(f"starting today {current_date_str} task")
                    stu = StuReportTask(user_config)
                    stu.run()

                    #tem = TemperatureTask(user_config)
                    # tem.run()

                    # we have completed today's task,then we need to update state
                    last_check_day = current_date_str
                    msg = f"Today's task has completed {user_config.user}"
                    logger.info(msg)
                    today_fail_count = 0
                    if mail_config.enable == 'true':
                        threading.Thread(
                            target=Notify, args=(mail_config, subject, msg,)).start()
                else:
                    today_fail_count += 1
                    logger.error(f"Login error, password or username wrong."
                                 f" Try times:{today_fail_count}")
            except Exception as e:
                today_fail_count += 1
                logger.error(
                    f"Task error, maybe can not access the internet {e}."
                    f" Try times: {today_fail_count}")
            finally:
                # retry many times, we should force exit this task.
                if today_fail_count > 10:
                    logger.error(f"Try many times, force exit")
                    # notify user task failed, please check network and config.
                    if mail_config.enable == 'true':
                        send_mail = threading.Thread(
                            target=Notify, args=(mail_config, subject, "Safe-Report task failed, please renew your config :-(",))
                        send_mail.start()
                        send_mail.join()
                        return
                # wait for 30 seconds, then retry again.
                time.sleep(30)
        else:
            logger.info("Not need to run today task, waiting for task")
            # wait for 20 minutes
            time.sleep(20*60)
