#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import numpy as np

from collections import OrderedDict


from config.settings import logger
from sans.data import Data
from sans.hfir.parser import HFIR as HFIRParser


#
# common metadata and detectors to all SANS HFIR instruments
#


'''
This HFIR generic! Just one detector!
'''


class HFIR(Data):

    metadata = OrderedDict({"title": "Header/Scan_Title",
                            "wavelength": "Header/wavelength",
                            "wavelength_spread": "Header/wavelength_spread"})

    # first detector is used for beam center
    detectors = OrderedDict({"main": "Data/Detector"})

    def __init__(self, filename):
        '''
        @param beam_center: [x,y] in pixels
        '''
        super(HFIR, self).__init__(filename)
        self._parse()

    def _parse(self):
        '''
        Main method that parses the XML file
        '''
        self._parser = HFIRParser(self._filename)
        for k, v in self.metadata.items():
            self.meta[k] = self._parser.getMetadata(v)
        for k, v in self.detectors.items():
            data_from_detector = self._parser.getData(v)
            self._add_detector_info_to_dataframe(k, data_from_detector)

    def _add_detector_info_to_dataframe(self, detector_name, detector_data):
        '''
        Creates or updates the Dataframe with the detector information
        '''
        n_rows, n_cols = detector_data.shape  # pos 0 rows, pos 1 columns
        total_size = n_rows * n_cols
        error = np.sqrt(detector_data)
        rows_v, cols_v = np.meshgrid(
            range(n_rows), range(n_cols), indexing='ij')

        d = {'name': np.full(total_size, detector_name, dtype=np.dtype('S32')),
             'i': rows_v.ravel(),  # i = rows
             'j': cols_v.ravel(),  # j = coluns
             'values': detector_data.ravel(),
             'errors': error.ravel(),
             }
        self.add_dictionary_as_dataframe(d)

    def place_detectors_in_space(self):
        '''
        Find beamcenter and adjust the axis
        Only does this for the main detector
        @param detector_list: Detector names.
        '''

        # common for all hfir just the main detector is used!
        detector_name = list(self.detectors.keys())[0]

        # First detector in list is used to find the beamcenter.
        beam_center_x, beam_center_y,  = self._find_beam_center(detector_name)
        self.meta["beam_center"] = [beam_center_x, beam_center_y]

        pixel_size_x = self._parser.getMetadata("Header/x_mm_per_pixel") * 1e-3
        pixel_size_y = self._parser.getMetadata("Header/y_mm_per_pixel") * 1e-3
        n_pixels_x = int(self._parser.getMetadata("Header/Number_of_X_Pixels"))
        n_pixels_y = int(self._parser.getMetadata("Header/Number_of_Y_Pixels"))
        sdd = self._parser.getMetadata("Motor_Positions/sdd")
        self.meta["sdd"] = sdd

        x_values = [pixel_size_x * i - beam_center_x *
                    pixel_size_x for i in range(n_pixels_x)]
        y_values = [pixel_size_y * i - beam_center_y *
                    pixel_size_y for i in range(n_pixels_y)]

        data_x, data_y = np.meshgrid(x_values, y_values, indexing='ij')

        d = {'x': data_x.ravel(),
             'y': data_y.ravel(),
             'z': np.full(len(data_x.ravel()), sdd)
             }

        df = pd.DataFrame(d)
        df = df.set_index(self.df[self.df.name == detector_name.encode('utf-8')].index)
        self.df = pd.concat([self.df, df], axis=1)

    def set_beam_center(self,beam_center_data):
        '''
        Copy x,y,z axes from beam_center_data
        '''
        self.df = pd.concat([self.df, beam_center_data.df[["x","y","z"]]], axis=1)

    def iq(self):
        '''
        Calculate I(Q)
        Q = 4 pi sin(theta) / lambda
        '''


        data_x = self.df.x.values
        data_y = self.df.y.values
        data_z = self.df.z.values
        angle = np.arctan2(data_y, data_x)
        angle = np.rad2deg(angle)
        # make it integer from 0 to 360
        angle = np.round(angle).astype(int) + 180


        q = np.linalg.norm(np.column_stack((data_x, data_y)), axis=1)


        angle_and_intensity_sum = np.bincount(angle,
            weights=data_z)
        angle_and_intensity_counts = np.bincount(angle)

        angle_and_intensity_average = angle_and_intensity_sum / angle_and_intensity_counts.astype(np.float64)
        angle_and_intensity_average = np.nan_to_num(angle_and_intensity_average) # because division by 0


        return angle_and_intensity_average
