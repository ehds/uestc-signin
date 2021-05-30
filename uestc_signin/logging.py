import logging
import os

log_dir = "logs"

def create_logger(name: str, path:str="log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    log_path = os.path.join(log_dir,path)
    fh = logging.FileHandler(log_path)
    sh = logging.StreamHandler()
    fh.setLevel(logging.INFO)
    # create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
    # add formatter to ch
    fh.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger