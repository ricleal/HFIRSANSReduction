'''
Created on Sep 7, 2016

@author: rhf
'''

from uncertainties import unumpy


def from_arrays_to_uncertainties(values,errors):
    res = unumpy.uarray(values,errors)
    return res

def from_uncertainties_to_arrays(uncertainties_array):
    v = unumpy.nominal_values(uncertainties_array)
    e = unumpy.std_devs(uncertainties_array)
    return v,e
