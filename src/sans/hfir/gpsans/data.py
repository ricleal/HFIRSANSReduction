'''
Created on Aug 26, 2016

@author: rhf
'''

from sans.hfir.data import HFIR
from config.settings import logger

class Data(HFIR):
    def __init__(self, filename):
        super(Data, self).__init__(filename)

    
        