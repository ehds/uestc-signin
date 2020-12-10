import sys
from uestc_signin.config import UserConfig, MailConfig, DEFAULT_CONFIG_PATH
from uestc_signin.task import MainTask
# TODO use argpase
if __name__ == "__main__":
    # setting logger
    import logging
    logging.basicConfig(format='%(asctime)s -%(name)s-%(levelname)s-%(message)s',
                        level=logging.INFO, filename='logs/uestc.log', filemode='a')
    config_path = DEFAULT_CONFIG_PATH
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    user_config = UserConfig(config_path)
    # get user config
    mail_config = MailConfig(config_path)
    # get user config

    enable_notify = mail_config.enable == 'true'
    # print(user_config,mail_config,enable_notify)
    MainTask(user_config, enable_notify)
