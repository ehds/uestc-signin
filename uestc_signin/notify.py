# -*- coding:utf-8 -*-
import smtplib
import os
import sys
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import logging
from config import MailConfig

logger = logging.getLogger(__name__)


class SendMail():
    def __init__(self, mail_config):
        self.host = mail_config.smtp_host
        self.port = mail_config.port
        self.username = mail_config.username
        self.password = mail_config.password
        self.receivers_str = mail_config.receivers
        self.enable = mail_config.enable
        self.is_login = False

    def login(self):
        if self.is_login:
            return True
        try:
            self.mail_handle = smtplib.SMTP(self.host, self.port)
            self.mail_handle.login(self.username, self.password)
        except Exception as e:
            logger.error(f'falied to login {e}')
            return False
        self.is_login = True
        return True

    def send_mail(self, subject, content='Success'):
        """
        @subject : the subject of the mail
        @content : what you would want to send
        """
        # get receivers and erase empty email
        # TODO check email format
        to_list = list(filter(lambda x: len(x) > 0,
                              self.receivers_str.split(',')))
        if len(to_list) == 0 or not self.login():
            return

        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        me = subject+'<'+self.username+'>'
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            self.mail_handle.sendmail(me, to_list, msg.as_string())
        except Exception as e:
            logger.error(f'failed to send mail {e}')
        self.mail_handle.close()

    def send_HTML(self, subject, content):
        to_list = self.receivers_str.split(',')
        if len(to_list) == 0 or not self.login():
            return
        msg = MIMEMultipart('alternatvie')
        me = subject + '<' + self.username + '>'
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ";".join(to_list)

        html = open('show.html').read()
        html += content+"</body></html>"
        print(html)
        html_part = MIMEText(html, 'html')
        html_part.set_charset('utf-8')
        msg.attach(html_part)
        try:
            self.mail_handle.sendmail(me, to_list, msg.as_string())
        except Exception as e:
            logger.error(f'failed to send mail {e}')
        self.mail_handle.close()


def Notify(mail_config, subject, msg):
    Mail = SendMail(mail_config)
    Mail.send_mail(subject, msg)


if __name__ == "__main__":
    mail_config = MailConfig("../uestc.conf")
    Notify(mail_config,"UESTC-Signin", "hello world")
