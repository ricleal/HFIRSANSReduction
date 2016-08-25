#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Aug 25, 2016

@author: rhf
'''

import os, sys
import json
import parser.parser
import importlib

from config.settings import logger, INSTRUMENT_CONFIGURATION

'''
Get's a parser and a data object 
'''

class Builder(object):
    
    def __init__(self, instrument_name, data_file):
        self._instrument_name = instrument_name
        self._data_file = data_file
    
    def set_configuration_dic(self):
        with open(INSTRUMENT_CONFIGURATION) as instrument_fp:
            instruments = json.load(instrument_fp)
        for instrument in instruments:
            if instrument["name"].lower() == self._instrument_name.lower():
                self._configuration = instrument
    
    
    def _get_class_from_string(self,full_module_class_path):
        
        module_name, class_name = full_module_class_path.rsplit(".", 1)
        MyClass = getattr(importlib.import_module(module_name), class_name)
        #instance = MyClass()
        return MyClass
    
    def build(self):
        
        parser = self._get_class_from_string(self.set_configuration_dic["parser"])
        
            
                
                

    
    def 

if __name__ == '__main__':
    pass