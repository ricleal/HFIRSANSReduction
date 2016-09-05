#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.ndimage as ndimage
from scipy import stats
from uncertainties import unumpy

from config.settings import logger

plt.rcParams['image.cmap'] = 'viridis'

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

    @staticmethod
    def _from_df_to_uncertainties(df):
        v = df['counts'].values
        e = df['errors'].values
        res = unumpy.uarray(v,e)
        return res

    def _from_uncertainties_to_df(self,uncertainties_array):
        self.df['counts'] = unumpy.nominal_values(uncertainties_array)
        self.df['errors'] = unumpy.std_devs(uncertainties_array)

    def __add__(self, other):
        un = Data._from_df_to_uncertainties(self.df)
        if isinstance(other, self.__class__):
            un_other = Data._from_df_to_uncertainties(other.df)
            res =  un + un_other
            self._from_uncertainties_to_df(res)
        else:
            res =  un + other
            self._from_uncertainties_to_df(res)
        return self

    def __sub__(self, other):
        un = Data._from_df_to_uncertainties(self.df)
        if isinstance(other, self.__class__):
            un_other = Data._from_df_to_uncertainties(other.df)
            res =  un - un_other
            self._from_uncertainties_to_df(res)
        else:
            res =  un - other
            self._from_uncertainties_to_df(res)
        return self

    def __mul__(self, other):
        un = Data._from_df_to_uncertainties(self.df)
        if isinstance(other, self.__class__):
            un_other = Data._from_df_to_uncertainties(other.df)
            res =  un * un_other
            self._from_uncertainties_to_df(res)
        else:
            res =  un * other
            self._from_uncertainties_to_df(res)
        return self

    def __itruediv__(self, other):
        un = Data._from_df_to_uncertainties(self.df)
        if isinstance(other, self.__class__):
            un_other = Data._from_df_to_uncertainties(other.df)
            res =  un / un_other
            self._from_uncertainties_to_df(res)
        else:
            res =  un / other
            self._from_uncertainties_to_df(res)
        return self

    def __floordiv__(self, other):
        # v1 // v2
        pass

    def __mod__(self, other):
        #self.data[k1] = v1 % v2
        pass

    def __pow__(self, other):
        # self.data[k1] = v1 ** v2
        pass

    # Let's override the data frame
    def __getitem__(self, key):
        val = self.df.__getitem__(key)
        return val

    def __setitem__(self, key, val):
        self.df.__setitem__(key, val)

    def __repr__(self):
        dictrepr = self.df.__repr__()
        return '%s(%s)' % (type(self).__name__, dictrepr)

    def add_dictionary_as_dataframe(self,d):
        df = pd.DataFrame(d)
        if self.df is None:
            self.df = df
        else:
            self.df = self.df.append(df, ignore_index=True)

    def get_detector_2d(self,detector_name = 'main', values_name = 'counts'):
        try:
            detector_name = detector_name.encode('utf-8')
        except AttributeError:
            pass
        pivot = self.df[self.df.name == detector_name].pivot(index='i', columns='j', values=values_name)
        return pivot.values

    def _find_beam_center(self,detector_name = "main"):
        '''
        Find center of mass given a detector_name
        @return: pixel coordinates
        '''
        data = self.get_detector_2d(detector_name)
        y,x = ndimage.measurements.center_of_mass(data)
        logger.info("Beam Center of Mass = (%f,%f) pixels."%(x,y))
        return x,y

    def plot(self, log=True):
        '''
        Main 2D plot
        If there's already a found beamcenter will plot a cross
        '''
        detector_names = self.df["name"].unique()
        plt.figure()
        subplot_prefix = "1{}".format(len(detector_names))
        for idx,detector_name in enumerate(detector_names):
            values = self.get_detector_2d(detector_name)
            if log:
                values = np.log(values)
            plt.subplot("{}{}".format(subplot_prefix,idx+1))
            plt.title(detector_name.decode())
            beam_center = self.meta.get("beam_center")
            if beam_center and detector_name.decode() == list(self.detectors.keys())[0]:
                # Modify the image to include the grid
                beam_center_x = int(round(beam_center[0]))
                beam_center_y = int(round(beam_center[1]))
                logger.debug("Setting plot cross at beam_center [%s,%s] pixels."%(beam_center_x,beam_center_y))
                values[:,beam_center_x] = values.max()
                values[beam_center_y,:] = values.max()
            if beam_center:
                x = self.df[self.df["name"] == detector_name].x.unique()
                y = self.df[self.df["name"] == detector_name].y.unique()
                extent=(x[0],x[-1],y.min(),y.max())
                plt.imshow(values,extent=extent, origin='upper', aspect='auto')
                plt.xlabel('X')
                plt.ylabel('Y')
            else:
                plt.imshow(values)
            plt.colorbar()
        plt.show()

    def plot_iq(self,n_bins=50):

        plt.figure()
        bin_means, bin_edges, binnumber = stats.binned_statistic(self.df['q'].values, self.df['counts'].values, statistic='mean', bins=n_bins)
        bin_width = (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[1:] - bin_width/2
        # normalize to 1
        bin_means = (bin_means - bin_means.min()) / (bin_means.max() - bin_means.min())
        plt.loglog(bin_centers,bin_means,'r--', label="binning")
        plt.show()

    def plot_iq_errors(self,n_bins=50):
        '''
        IQ with error propagation
        Note: this could have been done simply with:
        bin_means, bin_edges, binnumber = stats.binned_statistic(self.df['q'].values, self.df['counts'].values, statistic='mean', bins=n_bins)
        But it wouldn't have the errors in the mean.
        I am summing all the counts and error in every bin (sum of values => sum of errors) and then use the uncertainties package for division.
        '''

        plt.figure()
        x = self.df['q'].values
        y = self.df['counts'].values
        e = self.df['errors'].values

        # Let's get the histogram detail
        logger.debug("Binning Q.")

        occurrences_per_bin, bin_edges = np.histogram(x,bins=n_bins)
        bin_width = (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[1:] - bin_width/2

        # Return the indices of the bins to which each value in input array belongs.
        inds_x = np.digitize(x, bin_edges, right=True)
        # Don't know why but it puts a single value in the bin 0! Move it to pisition 1
        idx_to_remove = np.where(inds_x==0)[0]
        inds_x[idx_to_remove]=1

        # Error propagation: sum of values implies sum of errors
        values_sums_per_bin = np.bincount(inds_x, weights=y, minlength=len(bin_edges) - 1) #sums all values in every bin
        values_sums_per_bin = values_sums_per_bin[1:] # remove bin 0 (no counts!)

        error_sums_per_bin = np.bincount(inds_x, weights=e, minlength=len(bin_edges) - 1) #sums all errors in every bin
        error_sums_per_bin=error_sums_per_bin[1:] # remove bin 0 (no counts!)
        # Calculate average per bin (sum of the values divided by the cocurrences) with error propagation
        average_per_bin_un = unumpy.uarray(values_sums_per_bin,error_sums_per_bin) / occurrences_per_bin
        # Separate Values and error from the 2 arrays!
        values = unumpy.nominal_values(average_per_bin_un)
        errors = unumpy.std_devs(average_per_bin_un)

        plt.errorbar(bin_centers, values, yerr=errors, fmt='-', ecolor='g', capthick=2)
        plt.semilogx()
        plt.semilogy()
        plt.show()

    #
    # Corrections
    #

    def set_beam_center(self,beam_center_data):
        '''
        Copy x,y axes from beam_center_data
        z will be SDD.
        The beamcenter used can be collected at different distances
        '''
        self.df = pd.concat([self.df, beam_center_data.df[["x","y"]]], axis=1)
        d = {'z': np.full(self.df.shape[0], self.meta["sdd"])}
        df = pd.DataFrame(d)
        self.df = pd.concat([self.df, df], axis=1)

    def calculate_q_values(self):
        '''
        Calculate I(Q)
        Q = 4 pi sin(theta) / lambda
        Qx, Qy
        Theta
        '''
        data_x = self.df.x.values
        data_y = self.df.y.values
        data_z = self.df.z.values

        r = np.hypot(data_x, data_y)
        theta = np.arctan2(r, data_z)/2
        wavelength = self.meta["wavelength"]
        q = (4*np.pi/wavelength)*np.sin(theta)

        alpha = np.arctan2(data_x,data_y)
        qx = q*np.cos(alpha)
        qy = q*np.sin(alpha)

        d = {'theta' : theta,
            'q': q,
             'qx': qx,
             'qy': qy
             }
        df = pd.DataFrame(d)
        self.df = pd.concat([self.df, df], axis=1)


    def solid_angle_correction(self):
        '''
        General solid_angle with error propagation
        TODO: By detector

        '''
        #self.df['counts'] = self.df['counts'].values * np.cos(theta)**3
        theta = self.df.theta.values
        self *= np.cos(theta)**3


    def normalization(self, monitor=True, time=False):
        '''
        Either use monitor or time
        '''
        assert(monitor != time, "ERROR: monitor and time can not be both True or False.")
        if monitor:
            self /= self.meta["monitor_counts"]
        if time:
            self /= self.meta["counting_time"]


    def transmission_correction(self, transmission_value):
        '''
        Apply the transmission_value to the data
        @param transmission_value : value
        '''
        theta = self.df.theta.values
        self /= transmission_value**((1+(1/np.cos(2*theta)))/2)

    def calculate_transmission_value(self, direct_beam, radius=3.0):
        '''
        This should be used to calculare the transmission from the transmission date

        The sample transmission is calculated as the ratio Ts = Is/Ie, where Is and Ie are the accumulated
        detector counts for the Sample and Empty beam intensities, respectively, whereas the empty cell
        transmission is the ratio Tc=Ib/Ie where Ib is the intensity for the empty cell (Blank).

        @param direct_beam : direct beam data
        @return transmission_value
        '''
        sample_df = self.df[self.df[np.hypot(self.df.x, self.df.y) < radius]]
        # TODO
