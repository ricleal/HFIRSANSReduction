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
from operations.errors import compute as compute_uncertainties

from config.settings import logger
from .beam_center import find_beam_center

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
        self._filename = filename

    def __add__(self, other):
        if isinstance(other, self.__class__):
            self.df.counts = self.df.counts + other.df.counts
            self.df.errors = compute_uncertainties("x+y",
                values = {'x' : self.df.counts, 'y' :  other.df.counts},
                error_values = {'x' : self.df.errors, 'y' :  other.df.errors})
        else:
            self.df.counts = self.df.counts.values + other
        return self

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            self.df.counts = self.df.counts - other.df.counts
            self.df.errors = compute_uncertainties("x-y",
                values = {'x' : self.df.counts, 'y' :  other.df.counts},
                error_values = {'x' : self.df.errors, 'y' :  other.df.errors})
        else:
            self.df.counts = self.df.counts.values - other
        return self

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            self.df.counts = self.df.counts * other.df.counts
            self.df.errors = compute_uncertainties("x*y",
                values = {'x' : self.df.counts, 'y' :  other.df.counts},
                error_values = {'x' : self.df.errors, 'y' :  other.df.errors})
        else:
            self.df.counts = self.df.counts.values * other
        return self


    def __itruediv__(self, other):
        if isinstance(other, self.__class__):
            self.df.counts = self.df.counts / other.df.counts
            self.df.errors = compute_uncertainties("x/y",
                values = {'x' : self.df.counts, 'y' :  other.df.counts},
                error_values = {'x' : self.df.errors, 'y' :  other.df.errors})
        elif isinstance(other, tuple) and len(other) == 2:
            self.df.counts = self.df.counts.values / other[0]
            self.df.errors = compute_uncertainties("x/y",
                values = {'x' : self.df.counts, 'y' :  np.array(other[0])},
                error_values = {'x' : self.df.errors, 'y' :  np.array(other[1])})
        else:
            un = self.df.counts.values / other
            self.df.counts = un
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

    def __mean(self):
        sum_values = np.sqrt(np.sum(self.df.counts.values**2))
        # Error propagation of a sum is sqrt of squared sums
        sum_errors = np.sqrt(np.sum(self.df.errors.values**2))
        total = self.df.counts.dropna().size
        errors = compute_uncertainties("x/y",
            values = {'x' : np.array(sum_values), 'y' :  np.array(total)},
            error_values = {'x' : np.array(sum_errors), 'y' :  np.array(total)})
        return sum_values/total, errors

    def add_dictionary_as_dataframe(self,d):
        df = pd.DataFrame(d)
        if self.df is None:
            self.df = df
        else:
            self.df = self.df.append(df, ignore_index=True)

    def get_detector_2d(self,detector_name = 'main', values_name = 'counts'):
        '''
        Return values of uncertanities
        '''
        try:
            detector_name = detector_name.encode('utf-8')
        except AttributeError:
            pass
        pivot = self.df[self.df.name == detector_name].pivot(index='i', columns='j', values=values_name)
        values = pivot.values
        return values


    def _find_beam_center(self,detector_name = "main"):
        '''
        Find center of mass given a detector_name
        @return: pixel coordinates
        '''
        data = self.get_detector_2d(detector_name)
        x,y = find_beam_center(data)
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
            logger.debug("Plotting %s."%(detector_name))
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
        '''
        Just plots I(Q)
        '''
        logger.info("Plotting IQ.")
        plt.figure()
        counts = self.df['counts'].values
        bin_means, bin_edges, _ = stats.binned_statistic(self.df['q'].values, counts, statistic='mean', bins=n_bins)
        bin_width = (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[1:] - bin_width/2
        # normalize to 1
        bin_means = (bin_means - bin_means.min()) / (bin_means.max() - bin_means.min())
        plt.loglog(bin_centers,bin_means,'x', label="binning")
        plt.show()

    def plot_iq_errors(self,n_bins=50):
        '''
        IQ with error propagation
        Note: this could have been done simply with:
        bin_means, bin_edges, binnumber = stats.binned_statistic(self.df['q'].values, self.df['counts'].values, statistic='mean', bins=n_bins)
        But it wouldn't have the errors in the mean.
        I am summing all the counts and error in every bin (sum of values => sum of errors) and then use the uncertainties package for division.

        TODO: REFACTOR THIS!
        '''
        from uncertainties import unumpy

        logger.info("Plotting IQ with errors.")
        plt.figure()
        x = self.df['q'].values
        y, e = from_uncertainties_to_arrays(self.df['counts'].values)
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
        logger.info("Setting beam center.")

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
        logger.info("Calculate Q values.")

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


    def correct_solid_angle(self):
        '''
        General solid_angle with error propagation
        TODO: By detector

        '''
        logger.info("Solid Angle Correction.")
        #self.df['counts'] = self.df['counts'].values * np.cos(theta)**3
        theta = self.df.theta.values
        self *= np.cos(theta)**3


    def normalization(self, monitor=True):
        '''
        @param monitor: If True uses monitor_counts otherwise uses counting_time
        Either use monitor or time
        '''
        logger.info("Normalization.")
        if monitor:
            self /= self.meta["monitor_counts"]
        else:
            self /= self.meta["counting_time"]


    def correct_transmission(self, transmission_value):
        '''
        Apply the transmission_value to the data
        @param transmission_value : value
        '''
        logger.info("Transmission Correction.")
        theta = self.df.theta.values
        self /= transmission_value**((1+(1/np.cos(2*theta)))/2)

    def calculate_transmission_value(self, direct_beam, radius=3.0):
        '''
        This should be used to calculare the transmission from the transmission date

        The sample transmission is calculated as the ratio Ts = Is/Ie, where Is and Ie are the accumulated
        detector counts for the Sample and Empty beam intensities, respectively, whereas the empty cell
        transmission is the ratio Tc=Ib/Ie where Ib is the intensity for the empty cell (Blank).

        @param direct_beam : direct beam data
        @return transmission_value : float value!!!
        '''
        logger.info("Calculate Transmission value.")
        sample_df = self.df[self.df[np.hypot(self.df.x, self.df.y) < radius]]
        # TODO

    def mask_even(self):
        '''
        Front tubes???
        This needs to be revisited! Once masked the data is lost!!
        #TODO
        - Rename for front/back tubes
         - See if we can use Numpy MaskedArrays
        '''
        #self.df.loc[self.df.j%2 == 0, 'counts'] = np.nan
        logger.info("Mask Even tubes.")
        mask = self.df.j%2 == 0
        self.df.counts = self.df.counts.mask(mask)

    def mask_odd(self):
        '''
        Back tubes?
        '''
        #self.df.loc[(self.df.j+1)%2 == 0, 'counts'] = np.nan

        # # Mask NP version. Single array. Puts None in the mask :(
        # mask = (self.df.j+1)%2 == 0
        # masked_array = np.ma.masked_array(self.df.counts.values,mask=mask.values)
        # self.df.counts = np.ma.filled(masked_array)
        # print(self.df.counts)

        logger.info("Mask odd tubes.")
        mask = (self.df.j+1)%2 == 0
        self.df.counts = self.df.counts.mask(mask)



    def compute_sensitivity(self, min_sensitivity=0.5, max_sensitivity=1.5):
        '''
        Used if only for the flood data!!!

        SensitivityCorrection(flood_data, min_sensitivity=0.5, max_sensitivity=1.5)
        The relative detector efficiency is computed the following way

        S(x,y) = \frac{I_{flood}(x,y)}{1/N_{pixels} \ \sum_{i,j} \ I_{flood}(i,j)}
        where I_{flood}(x,y) is the pixel count of the flood data in pixel (x,y). If a minimum and/or maximum sensitivity is given, the pixels having an efficiency outside the given limits are masked and the efficiency is recomputed without using those pixels.
        The sample data is then corrected by dividing the intensity in each pixels by the efficiency S
        '''
        # First step
        logger.info("Compute Sensitivity.")

        #mean = self.df.counts.values.mean()
        mean = self.__mean()
        self /= mean

        # TODO: np.nanmean is not working!!!
        # Mask what is outside the boundaries
        mask = (self.df.counts < min_sensitivity) | (self.df.counts > max_sensitivity)
        if (mask.any()):
            logger.debug("There are values outside the limits [%s, %s]. Recomputing Sensitivity again...", min_sensitivity,max_sensitivity)
            self.df.counts = self.df.counts.mask(mask)
            # Same as mask using where
            # self.df.counts.where(((self.df.counts > min_sensitivity) & (self.df.counts < max_sensitivity)), np.nan, inplace=True)
            mean = np.nanmean(self.df.counts.values)
            self /= mean

    def correct_sensitivity(self,computed_sensitivity):
        '''
        Used for sample data!

        I'_{sample}(x,y) = \frac{I_{sample}(x,y)}{S(x,y)}
        The pixels found to have an efficiency outside the given limits are also masked in the sample data so that they don’t enter any subsequent calculations.
        '''
        logger.info("Sensitivity correction.")
        self /= computed_sensitivity
