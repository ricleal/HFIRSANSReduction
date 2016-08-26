#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import pandas as pd
import xarray as xr

from config.settings import logger
from sans.data import Data
from sans.hfir.parser import HFIR as HFIRParser 

#
# common metadata and data to all SANS HFIR instruments
#

metadata = {"title" : "Header/Scan_Title",
           "wavelength": "Header/wavelength",
           "wavelength_spread" : "Header/wavelength_spread"}

data = {"main" : "Data/Detector" }
detector_name = "main"

'''
This HFIR generic! Just one detector!
'''

class HFIR(Data):
    def __init__(self, filename, instrument_name, beam_center=None):
        '''
        @param beam_center: [x,y] in pixels
        '''
        super(HFIR, self).__init__(filename)
        self._parse()
        if beam_center:
            self._move_instrument(instrument_name, beam_center)
    
    def _parse(self):
        self._parser = HFIRParser(self._filename)
        for k, v in metadata.items():
            self.meta[k] = self._parser.getMetadata(v)
        for k, v in data.items():
            data_from_detector = self._parser.getData(v)
            self.data.update({k:data_from_detector})
    
    def _move_instrument(self, instrument_name,beam_center):
        this_dir = os.path.abspath(os.path.dirname(__file__))
        idf_filename = os.path.join(this_dir, instrument_name.lower(), instrument_name.lower() + ".hdf")
        self.df = pd.read_hdf(idf_filename, instrument_name)
        # self.df.info()
        self._set_detector_distance()
        self._set_detector_center(beam_center)
        self._set_data_axis()
        
    def _set_detector_distance(self, detector_name=detector_name):
        sdd = self._parser.getMetadata("Motor_Positions/sdd")
        logger.debug("Detector %s SDD = %f" %(detector_name, sdd))
        condition = self.df.name == detector_name.encode('utf-8')
        self.df.loc[(condition), 'z'] = sdd
        
    def _set_detector_center(self, beam_center, detector_name=detector_name):
        condition = self.df.name == detector_name.encode('utf-8')        
        self.df.loc[(condition), 'x'] = self.df[condition].i * self.df[condition].pixel_size_x  -  self.df[condition].pixel_size_x * beam_center[0]
        self.df.loc[(condition), 'y'] = self.df[condition].j * self.df[condition].pixel_size_y  -  self.df[condition].pixel_size_y * beam_center[1]
        logger.info("Center of the detector: %s" % self.df[condition & (self.df.x == 0) & (self.df.y == 0)][["i","j","z"]].values )
        
    def _set_data_axis(self, detector_name=detector_name):
        condition = self.df.name == detector_name.encode('utf-8')
        x = self.df[condition].x.unique()
        y = self.df[condition].y.unique()
        self.data[detector_name] = xr.DataArray(self.data[detector_name].values,
                                          [('y', y),
                                           ('x', x) ])
