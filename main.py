import sys
from uestc_signin.config import UserConfig
from uestc_signin.task import MainTask

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You need to set config path")
    # setting logger
    import logging
    logging.basicConfig(format='%(asctime)s -%(name)s-%(levelname)s-%(message)s', level=logging.INFO, filename='logs/uestc.log', filemode='a')
	# get user config
    config_path = sys.argv[1]
    config = UserConfig(config_path)
    MainTask(config)
