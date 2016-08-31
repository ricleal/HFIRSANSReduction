#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import os
import sys

import pandas as pd
import numpy as np

from mayavi import mlab



def main(filename)
    df = pd.read_hdf(filename, 'Data')

    #xyz = df[df.name == "wing"][["x","y","z"]].values
    xyz = df[["x","y","z"]].values

    x = xyz[:,0]
    y = xyz[:,1]
    z = xyz[:,2]

    # Plot scatter with mayavi
    figure = mlab.figure('Instrument View')
    mlab.points3d(x, y, z,mode='point')
    mlab.points3d([0], [0], [0],color=(1, 0, 0),scale_factor=0.1)
    mlab.axes()
    mlab.show()




if __name__ == '__main__':
    if len(sys.argv != 2):
        print "Usage %s <filename>"%sys.argv[0]
    else:
        filename = sys.argv[1]
        main(filename)
