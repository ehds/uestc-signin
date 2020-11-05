# encoding:utf-8

import requests
import base64

'''
手写文字识别
'''


def baidu_ocr(file_path):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=bl7DR1WXUaINikVf2zmQmoXz&client_secret=6tZzUcdKt9qw5q1sxaemP5tLMd0Nh3X7'
    response = requests.get(host)
    # get access_token
    access = None
    if response:
        access = response.json()["access_token"]

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"
    # 二进制方式打开图片文件
    f = open(file_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    request_url = request_url + "?access_token=" + access
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()["words_result"][0]["words"]
    return ""


if __name__ == "__main__":

    print(baidu_ocr("captcha.jpg"))
