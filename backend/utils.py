import logging

def setup_log():
    logging.basicConfig(level = logging.DEBUG,
        format = '[%(asctime)s] <%(levelname)s> %(message)s',
        datefmt = '%0H:%0M:%0S')

def log(msg, level = logging.DEBUG):
    logging.getLogger('__main__').log(level, msg)