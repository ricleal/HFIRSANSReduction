#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import json

from config.settings import logger
from parser.parser import HFIR

class Data(object):
    
    data = []
    detectors = []
    
    def __init__(self, filename):
        if not os.path.exists(filename):
            logger.error("File {} does not exist!".format(filename))
            return
        self._filename = filename
    

class HFIR(Data):
    def __init__(self, filename):
        super( HFIR, self ).__init__(filename)
        self._parser = HFIR
        
    def init(self):
        file_contents = 

class BioSans(HFIR):
    def __init__(self, filename):
        super( BioSans, self ).__init__(filename)
        self._instrument_name = "BioSANS"



def main(argv):
    d = BioSans("/HFIR/CG3/IPTS-17252/exp321/Shared/SVP/Edited_Datafiles/BioSANS_exp321_scan0050_0001.xml")
    logger.debug(dir(d))


if __name__ == "__main__":
    main(sys.argv)
    logger.info("Done!")
