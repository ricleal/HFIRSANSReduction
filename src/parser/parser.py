#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config.settings import logger

from abc import ABCMeta, abstractmethod
from pprint import pprint
import os, sys
import xml.etree.ElementTree as ET
import numpy as np
import json


LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))
instrument_file = os.path.join(LOCAL_DIR,'instruments.json')


class Parser(metaclass=ABCMeta):
    
    @abstractmethod
    def getMetadata(self, xpath):
        pass
    
    @abstractmethod
    def getData(self, xpath):
        pass
            

class XML(Parser):
    
    def __init__(self, filename):
        if not os.path.exists(filename):
            logger.error("File {} does not exist!".format(filename))
            sys.exit()
        
        self._root = self._parse(filename)
    
    def _parse(self, filename):
        logger.info("Parsing: %s."%filename)
        tree = ET.parse(filename)
        root = tree.getroot()
        return root            
               
class HFIR(XML):
    def getMetadata(self, xpath):
        elems = self._root.findall(xpath)
        if not elems:
            logger.error("xpath %s is not valid!")
            return None
        elif len(elems) >1:
            logger.warning("xpath %s has more than one element (len = %d)! Returning first!"%(xpath,len(elems)))
        return elems[0].text
    
    def getData(self,xpath):
        '''
        Parses the XML xpath data into a 2D array
        '''
        data_str = self.getMetadata(xpath)
        data_list_of_chars = [line.split("\t") for line in data_str.strip().split("\n")]
        data = [list(map(int, line)) for line in data_list_of_chars]
        data_np = np.array(data)
        # I have to confirm if the rotation is OK
        return np.rot90(data_np)
    
    

def main(argv):
    d = HFIR("/HFIR/CG3/IPTS-17252/exp321/Shared/SVP/Edited_Datafiles/BioSANS_exp321_scan0050_0001.xml")
    #print(d.getMetadata("Header/Instrument"))
    #print(d.getData("Data/Detector"))

if __name__ == "__main__":
    main(sys.argv)
    logger.info("Done!")

