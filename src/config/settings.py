'''
Created on Oct 29, 2015
@author: rhf
'''

import os
import logging
import logging.config

CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))
LOGGER_CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.cfg')
INSTRUMENT_CONFIGURATION = os.path.join(CONFIG_DIR, 'instruments.json')


def get_logger():
    logging.config.fileConfig(LOGGER_CONFIG_FILE, disable_existing_loggers=False)
    logger = logging.getLogger()
    return logger

logger = get_logger()
