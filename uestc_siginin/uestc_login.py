# coding:utf-8
import logging
import time
import json
import os
import base64
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from .baidu import baidu_ocr
from .captcha import CalcMoveOffset


class Login(object):
    def __init__(self, user, passwd, driver_name="firefox"):
        self.user = str(user)
        self.passwd = str(passwd)
        self.driver_name = driver_name
        self.driver = None
        self.timeout = 10  # second
        self.init_driver()

    def init_driver(self):
        if (self.driver_name == "firefox"):
            # set options
            options = webdriver.FirefoxOptions()
            # without GUI window
            #options.add_argument('--headless')
            cap = DesiredCapabilities().FIREFOX
            cap["marionette"] = True
            self.driver = webdriver.Firefox(
                options=options, capabilities=cap, executable_path='./driver/geckodriver')
            self.driver.implicitly_wait(self.timeout)

    def login(self) -> bool:
        if self.driver == None:
            return False

        driver = self.driver
        driver.implicitly_wait(10)

        driver.get(
            "https://mapp.uestc.edu.cn/site/uestcService/index?ticket=ST-150915-1u1eImAqIyPsxrugzxlf1590930369193-vuau-cas")
        # saving the login page
        time.sleep(5)
        logging.debug('finding login element')
        # # find usename and passwd element
        user = driver.find_element_by_id("username")
        passwd = driver.find_element_by_id("password")

        # login uestc
        login_btn = driver.find_element_by_class_name("auth_login_btn")

        user.send_keys(self.user)
        passwd.send_keys(self.passwd)

        logging.debug('clicking login button')
        login_btn.click()
        time.sleep(2)

        # complete captcha (move slider bar)
        # mabye fail we can try many times
        for i in range(20):
            captcha_img_ele = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div/canvas[1]')
            captcha_base64 = driver.execute_script(
                "return arguments[0].toDataURL('image/png').substring(21);", captcha_img_ele)
            width = driver.execute_script(
                "return arguments[0].width", captcha_img_ele)

            template_img_ele = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div/canvas[2]')
            template_base64 = driver.execute_script(
                "return arguments[0].toDataURL('image/png').substring(21);", template_img_ele)

            # decode
            origin_png = base64.b64decode(captcha_base64)
            with open("captcha.png", 'wb') as f:
                f.write(origin_png)

            template_png = base64.b64decode(template_base64)
            with open("template.png", 'wb') as f:
                f.write(template_png)

            offset = CalcMoveOffset('./captcha.png', 'template.png', width)
            print(width, offset)
            source = driver.find_element_by_class_name('slider')
            actions = ActionChains(
                driver).drag_and_drop_by_offset(source, offset, 0)
            actions.perform()
            # wating redirect if succes
            time.sleep(2)
            # vertify if login success
            if "authserver" not in driver.current_url:
                break
        # fail to login
        else:
            logging.error("log in failed,maybe username of password is wrong")
            return False

        driver.get(
            "http://eportal.uestc.edu.cn/qljfwapp/sys/lwReportEpidemicStu/*default/index.do#/dailyReport")
        time.sleep(2)
        cookies = driver.get_cookies()
        driver.quit()
        Login.save_cookies(cookies)
        return True

    @classmethod
    def save_cookies(cls, driver_cookies):
        cookies = {}
        for elem in driver_cookies:
            cookies[elem['name']] = elem['value']

        cookie_json = json.dumps(cookies, indent=4)
        with open("./data/cookies.json", "w") as f:
            f.write(cookie_json)

    @classmethod
    def load_cookies(cls):
        if not os.path.exists(os.path.join("./data/cookies.json")):
            return {}
        else:
            with open("./data/cookies.json", "r") as f:
                return json.load(f)


def ReLogin(config):
    if config.user is None or config.passwd is None:
        print("you need to set username and passwd")
        return False
    login = Login(config.user, config.passwd)
    if not login.login():
        print("login failed, please check your config!")
        return False
    print("Login success!")
    return True


if __name__ == "__main__":
    ReLogin()
