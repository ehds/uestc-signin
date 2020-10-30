import sys
from uestc_siginin.config import UserConfig
from uestc_siginin.task import MainTask

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You need to set config path")
    config_path = sys.argv[1]
    config = UserConfig(config_path)
    MainTask(config)
