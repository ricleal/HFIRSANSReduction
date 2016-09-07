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
from operations.errors import from_arrays_to_uncertainties

#
# common metadata and detectors to all SANS HFIR instruments
#


'''
This HFIR generic! Just one detector!
'''


class HFIR(Data):

    metadata = OrderedDict({"title": "Header/Scan_Title",
                            "wavelength": "Header/wavelength",
                            "wavelength_spread": "Header/wavelength_spread",
                            "sdd" : "Motor_Positions/sdd",
                            "monitor_counts" : "Counters/monitor",
                            "counting_time" : "Counters/time",
                            })

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
        # Parses metadata
        self._parser = HFIRParser(self._filename)
        for k, v in self.metadata.items():
            self.meta[k] = self._parser.getMetadata(v)
        # Parses the detector data
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
        
        counts = from_arrays_to_uncertainties(detector_data.ravel(),error.ravel())

        d = {'name': np.full(total_size, detector_name, dtype=np.dtype('S32')),
             'i': rows_v.ravel(),  # i = rows
             'j': cols_v.ravel(),  # j = coluns
             'counts': counts,
             }
        self.add_dictionary_as_dataframe(d)

    def place_detectors_in_space(self):
        '''
        Find beamcenter and adjust the axis
        Only does this for the main detector
        Starts from top left corner of the detector, Left hand coordinates
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
        sdd = self.meta["sdd"]

        pixel_x_middle = pixel_size_x/2
        pixel_y_middle = pixel_size_y/2

        # From left to right, negative to positive
        x_values = [pixel_x_middle + pixel_size_x * i - beam_center_x *
                    pixel_size_x for i in range(n_pixels_x)]
        # From top to bottom,  positive to negative
        y_values = [pixel_y_middle + pixel_size_y * i - (n_pixels_y - beam_center_y) *
                    pixel_size_y for i in reversed(range(n_pixels_y))]

        data_x, data_y = np.meshgrid(x_values, y_values)

        d = {'x': data_x.ravel(),
             'y': data_y.ravel(),
             'z': np.full(len(data_x.ravel()), sdd)
             }

        df = pd.DataFrame(d)
        df = df.set_index(self.df[self.df.name == detector_name.encode('utf-8')].index)
        self.df = pd.concat([self.df, df], axis=1)
