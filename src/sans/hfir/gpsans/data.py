'''
Created on Aug 26, 2016

@author: rhf
'''

from sans.hfir.data import HFIR
from config.settings import logger

class Data(HFIR):
    def __init__(self, filename, move_instrument=False):
        instrument_name = "GPSANS"
        super(Data, self).__init__(filename,instrument_name,move_instrument)

    
        