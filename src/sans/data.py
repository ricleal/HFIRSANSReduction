#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import json
from collections import OrderedDict

from config.settings import logger
from parser.parser import HFIR

class Data(object):
    
    
    data = OrderedDict()
    instrument_df = None
    
    def __init__(self, filename, move_instrument=False):
        if not os.path.exists(filename):
            logger.error("File {} does not exist!".format(filename))
            return
        self._filename = filename
        self._move_instrument = move_instrument
    
    
    def __add__(self, other):
        for k1,v1,_,v2 in zip(self.data,other.data):
            self.data[k1] = v1 + v2
    
    def __sub__(self, other):
        for k1,v1,_,v2 in zip(self.data,other.data):
            self.data[k1] = v1 - v2
    
    def __mul__(self, other):
        for k1,v1,_,v2 in zip(self.data,other.data):
            self.data[k1] = v1 * v2
    
    def __floordiv__(self, other):
        for k1,v1,_,v2 in zip(self.data,other.data):
            self.data[k1] = v1 // v2
    
    def __div__(self, other):
        for k1,v1,_,v2 in zip(self.data,other.data):
            self.data[k1] = v1 / v2
    
    def __mod__(self, other):
        for k1,v1,_,v2 in zip(self.data,other.data):
            self.data[k1] = v1 % v2

    def __pow__(self, other):
        for k1,v1,_,v2 in zip(self.data,other.data):
            self.data[k1] = v1 ** v2

    def solid_angle(self):
        pass
    
    def beam_center(self):
        # return [x,y,z]
        pass
    
    