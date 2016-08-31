'''
Created on Aug 26, 2016

@author: rhf
'''

import numpy as np

from config.settings import logger
from ..parser import XML


class HFIR(XML):
    def getMetadata(self, xpath):
        '''
        Given Xpath returns either float or string
        '''
        elems = self._root.findall(xpath)
        if not elems:
            logger.error("xpath %s is not valid!"%xpath)
            return None
        elif len(elems) >1:
            logger.warning("xpath %s has more than one element (len = %d)! Returning first!"%(xpath,len(elems)))
        value_as_string = elems[0].text
        try:
            return float(value_as_string)
        except ValueError:
            return value_as_string

        return

    def getData(self,xpath):
        '''
        Parses the XML xpath data into a 2D Xarray
        '''
        data_str = self.getMetadata(xpath)
        data_list_of_chars = [line.split("\t") for line in data_str.strip().split("\n")]
        data = [list(map(int, line)) for line in data_list_of_chars]
        data_np = np.array(data)
        data_np = np.rot90(data_np)
        data_np = np.flipud(data_np)
        return data_np
