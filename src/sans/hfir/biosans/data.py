'''
Created on Aug 26, 2016

@author: rhf
'''

import numpy as np
import pandas as pd

from sans.hfir.data import HFIR
from config.settings import logger

def calculate_neutron_gravitational_drop(path_length, wavelength):
    '''
    Calculate the gravitational drop of the neutrons
    path_length in meters
    wavelength in Angstrom
    '''
    wavelength *= 1e-10
    neutron_mass = 1.674927211e-27
    gravity = 9.80665
    h_planck = 6.62606896e-34
    l_2 = (gravity * neutron_mass**2 / (2.0 * h_planck**2 )) * path_length**2
    return wavelength**2 * l_2

class Data(HFIR):

    def __init__(self, filename):
        self.detectors.update({"wing" : "Data/DetectorWing" })
        super(Data, self).__init__(filename)

    def place_detectors_in_space(self):
        '''
        Calls generic hfir and finds beamcenter
        Than positions the wing detector
        '''

        # This will center the main detector
        super(Data, self).place_detectors_in_space()

        pixel_size_x = self._parser.getMetadata("Header/x_mm_per_pixel") * 1e-3
        pixel_size_y = self._parser.getMetadata("Header/y_mm_per_pixel") * 1e-3
        n_pixels_x = int(self._parser.getMetadata("Header/west_wing_number_of_x_Pixels"))
        n_pixels_y = int(self._parser.getMetadata("Header/west_wing_number_of_y_Pixels"))
        radius = self._parser.getMetadata("Header/west_wing_det_radius_m")
        rotation = self._parser.getMetadata("Motor_Positions/det_west_wing_rot")

        step = 0.0055
        step_angle_radians = np.arcsin(step/2.0/radius)
        step_angle_degrees = np.degrees(step_angle_radians)

        radial_angles = [ np.deg2rad(90) - np.deg2rad(rotation) + -step_angle_radians * i for i in range(n_pixels_x) ]
        row_z = radius*np.cos(radial_angles)
        row_x = radius*np.sin(radial_angles)

        beam_center_y = self.meta["beam_center"][1]
        pixel_y_middle = pixel_size_y/2
        row_y = [pixel_size_y*i + pixel_y_middle - ((n_pixels_y - beam_center_y) * pixel_size_y) for i in range(n_pixels_y) ]
        y_drop = self.gravity_drop()
        row_y = np.array(row_y) + y_drop


        data_x,data_y = np.meshgrid(row_x, row_y)
        data_z = np.tile(row_z,len(row_y))

        d = {'x': data_x.ravel(),
             'y': data_y.ravel(),
             'z': data_z,
             }

        df = pd.DataFrame(d)
        df = df.set_index(self.df[self.df.name == "wing".encode('utf-8')].index)
        # We are assigning rows because we have alread x,y,z for main detector
        self.df.loc[self.df.name == "wing".encode('utf-8'),['x','y','z']] = df

    def gravity_drop(self):
        sdd = self.meta["sdd"]
        wavelength = self.meta["wavelength"]
        radius = self._parser.getMetadata("Header/west_wing_det_radius_m")
        path_length = sdd - radius;
        y_drop = calculate_neutron_gravitational_drop(path_length,wavelength)
        logger.info("Correcting for gravity: %f m"%y_drop)
        return y_drop
