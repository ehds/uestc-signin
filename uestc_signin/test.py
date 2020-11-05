# encoding:utf-8

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
from baidu import baidu_ocr
import time
import logging
import pickle
import base64
from captcha import CalcMoveOffset

USERNAME="x"
PASSWD = "x"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./uestc.log',
                    filemode='w')

options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
driver = webdriver.Firefox(options=options, capabilities=cap, executable_path='./driver/geckodriver')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
cus_headers = {
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive"
}
logging.debug('logging in uestc')
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (headers["User-Agent"])
# dcap["phantomjs.page.customHeaders"] = cus_headers
# driver = webdriver.PhantomJS("C:/Users/ehds/Desktop/daka/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe",desired_capabilities=dcap)
driver.get("https://mapp.uestc.edu.cn/site/uestcService/index?ticket=ST-150915-1u1eImAqIyPsxrugzxlf1590930369193-vuau-cas")
# driver.get("https://www.bilibili.com/bangumi/play/ep326710")

time.sleep(2)
driver.get_screenshot_as_file("./screenshot.png")
logging.debug('finding element')
# # find usename and passwd element


user = driver.find_element_by_id("username")
passwd = driver.find_element_by_id("password")
# need vertify captch
# captch_code =str(baidu_ocr("captcha.jpg"))
login_btn = driver.find_element_by_class_name("auth_login_btn")
user.send_keys(USERNAME)
passwd.send_keys(PASSWD)
logging.debug('clicking login button')
login_btn.click()
time.sleep(3)

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

source = driver.find_element_by_class_name('slider')
actions = ActionChains(driver).drag_and_drop_by_offset(source, offset, 0)
actions.perform()
time.sleep(10)
driver.quit()
