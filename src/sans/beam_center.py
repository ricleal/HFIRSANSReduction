#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.ndimage as ndimage
from scipy import stats
import scipy.optimize as opt

from config.settings import logger

'''
Created on Aug 25, 2016

@author: rhf
'''

from numpy import *
from scipy import optimize

'''
gaussian 2D fitting from:
http://scipy.github.io/old-wiki/pages/Cookbook/FittingData
'''
def gaussian(height, center_x, center_y, width_x, width_y):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*exp(
                -(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2)

def moments(data):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution by calculating its
    moments """
    total = data.sum()
    X, Y = indices(data.shape)
    x = (X*data).sum()/total
    y = (Y*data).sum()/total
    col = data[:, int(y)]
    width_x = sqrt(abs((arange(col.size)-y)**2*col).sum()/col.sum())
    row = data[int(x), :]
    width_y = sqrt(abs((arange(row.size)-x)**2*row).sum()/row.sum())
    height = data.max()
    return height, x, y, width_x, width_y

def fitgaussian(data):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution found by a fit"""
    params = moments(data)
    errorfunction = lambda p: ravel(gaussian(*p)(*indices(data.shape)) -
                                 data)
    p, success = optimize.leastsq(errorfunction, params)
    return p

'''
Find beam center methods

'''

def find_center_of_mass(data_2d):
    '''
    Somehow unreliable
    '''
    center_guess_y,center_guess_x = ndimage.measurements.center_of_mass(data_2d)
    logger.info("Beam Center of Mass = (%2f,%2f) pixels."%(center_guess_x,center_guess_y))
    return center_guess_x,center_guess_y

def find_maxs_along_axes(data_2d):
    '''
    Works well!
    '''
    x_sums = np.sum(data_2d, axis=1)
    print(x_sums)
    x_max_index = np.argmax(x_sums)
    y_sums = np.sum(data_2d, axis=0)
    print(y_sums)
    y_max_index = np.argmax(y_sums)
    logger.info("Beam Maximums along axes = (%2f,%2f) pixels."%(x_max_index,y_max_index))
    return y_max_index, x_max_index

def fit_gaussian(data_2d):
    params = fitgaussian(data_2d)
    _, x, y, _, _ = params
    logger.info("Beam Gaussian Fit = (%2f,%2f) pixels."%(x,y))
    return y,x

'''
Pick a method from the top

#TODO : Need to have a beam method selection here
'''
def find_beam_center(data_2d):
    '''
    Find center of mass given a detector_name
    @param data :: 2D array
    @return: pixel coordinates
    '''
    #return find_center_of_mass(data_2d)
    return fit_gaussian(data_2d)
