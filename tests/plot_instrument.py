#!/usr/bin/env python2

import pandas as pd
import os
import numpy as np
from mayavi import mlab

LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(LOCAL_DIR, "../src/instrument/biosans.hdf")
        

df = pd.read_hdf(data_file, 'BioSANS')

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