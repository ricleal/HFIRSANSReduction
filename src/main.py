#!/usr/bin/env python3

'''
Created on Aug 25, 2016

@author: rhf
'''

from pprint import pprint


def gpsans():
    from sans.hfir.gpsans.data import Data
    #d = Data("/HFIR/CG2/IPTS-17367/exp137/Datafiles/CG2_exp137_scan0001_0001.xml")
    bc = Data("/tmp/CG2_exp137_scan0067_0001.xml")
    bc.place_detectors_in_space()
    #bc.plot()

    data = Data("/tmp/CG2_exp137_scan0066_0001.xml")
    data.set_beam_center(bc)
    data.plot()

    data.calculate_q_values()
    data.solid_angle_correction()
    #print(data.df)
    data.plot_iq()

def biosans():
    from sans.hfir.biosans.data import Data
    #bc = Data("/HFIR/CG3/IPTS-0000/exp327/Datafiles/BioSANS_exp327_scan0039_0001.xml")
    bc = Data("/Users/rhf/Dropbox (ORNL)/DocumentsWorkstation/SANS/BioSans/20160621-SensitivityCorrupted/BioSANS_exp318_scan0185_0001.xml")
    bc.place_detectors_in_space()
    #bc.plot()

#     data = Data("/HFIR/CG3/IPTS-0000/exp327/Datafiles/BioSANS_exp327_scan0045_0001.xml")
    data = Data("/Users/rhf/Dropbox (ORNL)/DocumentsWorkstation/SANS/BioSans/20160621-SensitivityCorrupted/BioSANS_exp318_scan0034_0001.xml")
    data.set_beam_center(bc)
#    data.plot()
    data.calculate_q_values()
    data.solid_angle_correction()
    #print(data.df)
    data.plot_iq()


def main():
    gpsans()
    #biosans()


if __name__ == "__main__":
    main()
