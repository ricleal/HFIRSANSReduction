'''
Created on Aug 25, 2016

@author: rhf


Standalone script

    Generate Pandas IDF
    For every detector:
        name, parent, i, j, x, y, z, pixel_size_x, pixel_size_y
'''

import numpy as np
import pandas as pd
import os

from config.settings import logger

columns= ('name', 'parent', 'i', 'j', 'x', 'y', 'z', 'pixel_size_x', 'pixel_size_y')

def generate_bio_sans():
    
    instrument_name = "biosans"
    
    det1_name = "main"
    det1_n_pixels_x = 192
    det1_n_pixels_y = 256
    det1_pixel_width = 5.5e-3
    det1_pixel_height = 4.0e-3
    det1_distance = 10
    
    det2_name = "wing"
    det2_n_pixels_x = 160
    det2_n_pixels_y = 256
    det2_pixel_width = 5.5e-3
    det2_pixel_height = 4.0e-3
    det2_radius = 1.13
    
    det2_step = 0.0055
    det2_step_angle_radians = np.arcsin(det2_step/2.0/det2_radius)
    det2_step_angle_degrees = np.degrees(det2_step_angle_radians)
    
    
    idf_filepath = os.path.join("../sans/hfir", instrument_name, instrument_name + '.hdf')
    
    #
    # det 1
    #
    data_i, data_j = np.meshgrid(range(det1_n_pixels_x),range(det1_n_pixels_y))
    data_i, data_j = data_i.ravel(), data_j.ravel()
    
    pixel_x_middle = det1_pixel_width/2
    row_x = [pixel_x_middle*(i+1) - det1_n_pixels_x*pixel_x_middle/2 for i in range(det1_n_pixels_x) ]
    pixel_y_middle = det1_pixel_height/2
    row_y = [pixel_y_middle*(i+1) - det1_n_pixels_y*pixel_y_middle/2 for i in range(det1_n_pixels_y) ]
    data_x, data_y = np.meshgrid(row_x,row_y)
    data_x, data_y = data_x.ravel(), data_y.ravel()
    
    det1_data = np.vstack([np.full(data_i.shape,det1_name, dtype=np.dtype('a4')), # Name
                      np.empty_like(data_i),
                      data_i,
                      data_j,
                      data_x,
                      data_y,
                      np.full(data_i.shape,det1_distance),
                      np.full(data_i.shape,det1_pixel_width),
                      np.full(data_i.shape,det1_pixel_height),
                      ])
    #
    # det 2
    #    
    
    data_i, data_j = np.meshgrid(range(det2_n_pixels_x),range(det2_n_pixels_y))
    data_i, data_j = data_i.ravel(), data_j.ravel()
    
    radial_angles = [ -det2_step_angle_radians * i for i in range(det2_n_pixels_x) ]
    row_z = det2_radius*np.cos(radial_angles)
    row_x = det2_radius*np.sin(radial_angles)
    
    pixel_y_middle = det2_pixel_height/2
    row_y = [pixel_y_middle*(i+1) - det2_n_pixels_y*pixel_y_middle/2 for i in range(det2_n_pixels_y) ]    
    
    data_x,data_y = np.meshgrid(row_x,row_y)
    data_x,data_y = data_x.ravel(),data_y.ravel(),
    data_z = np.tile(row_z,len(row_y)) 
    
    
    
    
    det2_data = np.vstack([np.full(data_i.shape,det2_name, dtype=np.dtype('a4')), # Name
                      np.empty_like(data_i),
                      data_i,
                      data_j,
                      data_x,
                      data_y,
                      data_z,
                      np.full(data_i.shape,det2_pixel_width),
                      np.full(data_i.shape,det2_pixel_height),
                      ])
    
    #
    # Stack and save
    #
    data = np.hstack([det1_data, det2_data])
    
    df = pd.DataFrame(data.T, columns=columns)
    df[['i', 'j', 'x', 'y', 'z', 'pixel_size_x', 'pixel_size_y']] = df[['i', 'j', 'x', 'y', 'z', 'pixel_size_x', 'pixel_size_y']].apply(pd.to_numeric,errors='ignore')
    
    df.info()
    
    df.to_hdf(idf_filepath, instrument_name)
    logger.info("IDF saved to: %s."%idf_filepath)


def generate_gp_sans():
    
    instrument_name = "gpsans"
    
    det1_name = "main"
    det1_n_pixels_x = 192
    det1_n_pixels_y = 256
    det1_pixel_width = 5.5e-3
    det1_pixel_height = 4.0e-3
    det1_distance = 10
    
    
    idf_filepath = os.path.join("../sans/hfir", instrument_name, instrument_name + '.hdf')
    
    #
    # det 1
    #
    data_i, data_j = np.meshgrid(range(det1_n_pixels_x),range(det1_n_pixels_y))
    data_i, data_j = data_i.ravel(), data_j.ravel()
    
    pixel_x_middle = det1_pixel_width/2
    row_x = [pixel_x_middle*(i+1) - det1_n_pixels_x*pixel_x_middle/2 for i in range(det1_n_pixels_x) ]
    pixel_y_middle = det1_pixel_height/2
    row_y = [pixel_y_middle*(i+1) - det1_n_pixels_y*pixel_y_middle/2 for i in range(det1_n_pixels_y) ]
    data_x, data_y = np.meshgrid(row_x,row_y)
    data_x, data_y = data_x.ravel(), data_y.ravel()
    
    det1_data = np.vstack([np.full(data_i.shape,det1_name, dtype=np.dtype('a4')), # Name
                      np.empty_like(data_i),
                      data_i,
                      data_j,
                      data_x,
                      data_y,
                      np.full(data_i.shape,det1_distance),
                      np.full(data_i.shape,det1_pixel_width),
                      np.full(data_i.shape,det1_pixel_height),
                      ])
    
    #
    # Stack and save
    #
    data = det1_data
    
    df = pd.DataFrame(data.T, columns=columns)
    df[['i', 'j', 'x', 'y', 'z', 'pixel_size_x', 'pixel_size_y']] = df[['i', 'j', 'x', 'y', 'z', 'pixel_size_x', 'pixel_size_y']].apply(pd.to_numeric,errors='ignore')
    
    df.info()
    
    df.to_hdf(idf_filepath, instrument_name)
    logger.info("IDF saved to: %s."%idf_filepath)
    
if __name__ == "__main__":
    generate_bio_sans()
    generate_gp_sans()
    
    