import logging
from os import makedirs
from os.path import abspath, join

def set_logger(save_dir:str='./', log_name:str='logfile', is_stream:bool=False):
    makedirs(save_dir, exist_ok=True)
    log_path = abspath(join(save_dir, f'{log_name}.log'))
    filehandler = logging.FileHandler(log_path, encoding='utf-8')
    logformat = logging.Formatter('[%(asctime)s] %(message)s')
    filehandler.setFormatter(logformat)
    
    logger = logging.getLogger('log')
    logger.setLevel(logging.INFO)
    logger.addHandler(filehandler)
    
    if is_stream:
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(logformat)
        logger.addHandler(streamhandler)
        
    return logger