import logging

def set_logger(dir:str):
    filehandler = logging.FileHandler(
        f'{dir}/test_log.log'
    )
    #streamhandler = logging.StreamHandler()

    logfomat = logging.Formatter('[%(asctime)s] %(message)s')
    filehandler.setFormatter(logfomat)
    #streamhandler.setFormatter(logfomat)

    logger = logging.getLogger('log')
    logger.setLevel(logging.INFO)
    logger.addHandler(filehandler)
    #logger.addHandler(streamhandler)

    return logger