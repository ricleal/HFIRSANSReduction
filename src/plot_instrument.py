#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import os
import sys

import pandas as pd
import numpy as np

'''
Plot instrument in 3D

Needs an HDF file saved as:

data.df.to_hdf("/tmp/biosans.hdf","data")

'''



def main(filename):
    df = pd.read_hdf(filename, 'data')

    #xyz = df[df.name == "wing"][["x","y","z"]].values
    xyz = df[["x","y","z"]].values

    x = xyz[:,0]
    y = xyz[:,1]
    z = xyz[:,2]

    # # Plot scatter with mayavi
    # from mayavi import mlab
    # figure = mlab.figure('Instrument View')
    # mlab.points3d(x, y, z,mode='point')
    # mlab.points3d([0], [0], [0],color=(1, 0, 0),scale_factor=0.1)
    # mlab.axes()
    # mlab.show()

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x[::50], y[::50], z[::50],c='b', marker='.')
    ax.scatter(0,0,0,c='r', marker='o')
    ax.view_init(270, 270)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage %s <filename>"%sys.argv[0])
    else:
        filename = sys.argv[1]
        main(filename)
