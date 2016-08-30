#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.ndimage as ndimage


from config.settings import logger


class Data(object):
    '''
    Abstract class that represents the data object (workspace)
    '''


    df = None # Instrument data frame
    meta = {}

    def __init__(self, filename):
        if not os.path.exists(filename):
            logger.error("File %s does not exist!"%(filename))
            sys.exit()
        logger.info("Using file %s."%(filename))
        self._filename = filename

    def __add__(self, other):
        self.df.values += other.values
        self.df.errors = np.sqrt(self.df.errors**2 + other.errors**2)

    def __sub__(self, other):
        self.df.values -= other.values
        self.df.errors = np.sqrt(self.df.errors**2 + other.errors**2)

    def __mul__(self, other):
        self.df.values *= other.values
        # TODO ERROR Propagation

    def __floordiv__(self, other):
        # v1 // v2
        pass

    def __div__(self, other):
        pass

    def __mod__(self, other):
        #self.data[k1] = v1 % v2
        pass

    def __pow__(self, other):
        # self.data[k1] = v1 ** v2
        pass


    def add_dictionary_as_dataframe(self,d):
        df = pd.DataFrame(d)
        if self.df is None:
            self.df = df
        else:
            self.df = self.df.append(df, ignore_index=True)


    def _get_detector_2d(self,detector_name, values_name = 'values'):
        try:
            detector_name = detector_name.encode('utf-8')
        except AttributeError:
            pass
        pivot = self.df[self.df.name == detector_name].pivot(index='i', columns='j', values=values_name)
        return pivot.values

    def solid_angle(self):
        pass

    def _find_beam_center(self,detector_name = "main"):
        '''
        Find center of mass given a detector_name
        @return: pixel coordinates
        '''
        data = self._get_detector_2d(detector_name)
        y,x = ndimage.measurements.center_of_mass(data)
        logger.info("Beam Center of Mass = (%f,%f) pixels."%(x,y))
        return x,y


    def plot(self):
        detector_names = self.df["name"].unique()
        plt.figure()
        subplot_prefix = "1{}".format(len(detector_names))
        for idx,detector_name in enumerate(detector_names):
            values = self._get_detector_2d(detector_name)
            plt.subplot("{}{}".format(subplot_prefix,idx+1))
            plt.title(detector_name.decode())
            beam_center = self.meta.get("beam_center")
            if beam_center and detector_name.decode() == list(self.detectors.keys())[0]:
                # Modify the image to include the grid
                values[:,round(beam_center[0])] = values.max()
                values[round(beam_center[1]),:] = values.max()
            plt.imshow(values)
            plt.colorbar()
        plt.show()

#     def plot_one_color_bar(self):
#         detector_names = self.df["name"].unique()
#         fig, axes = plt.subplots(nrows=1, ncols=len(detector_names))
#         for ax,detector_name in zip(axes.flat,detector_names):
#             data = self._get_detector_2d(detector_name)
#             im = ax.imshow(data)
#             ax.set_title(detector_name.decode())
#         fig.colorbar(im, ax=axes.ravel().tolist())
#         plt.show()
