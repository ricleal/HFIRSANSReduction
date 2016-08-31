#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.ndimage as ndimage
from scipy import stats

from config.settings import logger

'''
Created on Aug 25, 2016

@author: rhf
'''

def find_beam_center(self,data):
    '''
    Find center of mass given a detector_name
    @param data :: 2D array
    @return: pixel coordinates
    '''

    y,x = ndimage.measurements.center_of_mass(data)
    logger.info("Beam Center of Mass = (%f,%f) pixels."%(x,y))

    initial_guess = (500, x, y, 4, 4, 0, 0)
    popt, pcov = opt.curve_fit(twoD_Gaussian, (x, y),
                               data.ravel(), p0=initial_guess)


    xv, yv = meshgrid(data.shape[0], data.shape[1])

    fit = _twoD_Gaussian((xv, yv), *popt)
    x_diff = (popt[1] - int(round(popt[1])))*pixel_size_y
    y_diff = (popt[2] - int(round(popt[2]))) * pixel_size_x
    center_x = center_data.coords['y'].values[int(round(popt[1]))] + x_diff
    center_y = center_data.coords['x'].values[int(round(popt[2]))] + y_diff
    return center_x, center_y, popt[1], popt[2]




def _twoD_Gaussian(xdata_tuple, amplitude, xo, yo,
                  sigma_x, sigma_y, theta, offset):
    """
    2D Gaussian function
    from http://stackoverflow.com/questions/21566379/fitting-a-2d-gaussian
        -function-using-scipy-optimize-curve-fit-valueerror-and-m
    """
    (x, y) = xdata_tuple
    a = ((np.cos(theta)**2)/(2*sigma_x**2) +
         (np.sin(theta)**2)/(2*sigma_y**2))
    b = (-(np.sin(2*theta))/(4*sigma_x**2) +
          (np.sin(2*theta))/(4*sigma_y**2))
    c = ((np.sin(theta)**2)/(2*sigma_x**2) +
         (np.cos(theta)**2)/(2*sigma_y**2))
    g = offset + amplitude*np.exp(- (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) +
                                     c*((y-yo)**2)))
    return g.ravel()
