# coding:utf-8

import time

def get_date_str():
   return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())



if __name__ == "__main__":
    print(get_date_str())