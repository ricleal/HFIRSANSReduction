#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from collections import OrderedDict

from config.settings import logger
import matplotlib.pyplot as plt
import numpy as np

class Data(object):
    '''
    Abstract class that represents the data object (workspace)
    '''
    
    data = OrderedDict()
    meta = {}
    df = None # Instrument data frame
    
    def __init__(self, filename):
        if not os.path.exists(filename):
            logger.error("File %s does not exist!"%(filename))
            return
        self._filename = filename    
    
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
    
    def plot(self):
        for idx,d in enumerate(self.data.values()):
            #d.plot.contourf(origin = 'lower')
            #d.plot.plot.pcolormesh()
            #d.plot()
            #d.plot.imshow(origin = 'lower')
            
            #X, Y = np.meshgrid(d.coords["x"].values,d.coords["y"].values)
            #plt.pcolormesh(X,Y,d.values,origin="upper")
            
            plt.subplot(len(self.data), 1, idx+1)
            x = d.coords["x"].values
            y = d.coords["y"].values
            values = np.fliplr(d.values)
            plt.imshow(values,extent=[x.max(), x.min(), y.min(),y.max()])
        plt.show()
        
        
    
    