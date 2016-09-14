#!/usr/bin/env python3

'''
Created on Aug 25, 2016

@author: rhf
'''

from pprint import pprint
import copy

def gpsans():
    from sans.hfir.gpsans.data import Data
    bc = Data("/HFIR/CG2/IPTS-17367/exp137/Datafiles/CG2_exp137_scan0067_0001.xml")
    #bc = Data("/Users/rhf/tmp/CG2_exp137_scan0067_0001.xml")
    bc.place_detectors_in_space()
    #bc.plot()
    #print(bc.df)

    #data = Data("/Users/rhf/tmp/CG2_exp137_scan0066_0001.xml")
    data = Data("/HFIR/CG2/IPTS-17367/exp137/Datafiles/CG2_exp137_scan0066_0001.xml")
    data.set_beam_center(bc)

    data.calculate_q_values()
    #print(data.df[["counts","errors"]][100:110])
    data.correct_solid_angle()
    #print(data.df[["counts","errors"]][100:110])
    #print(data.df)
    data.plot_iq()
    data.plot_iq_errors()
    data.normalization()
    data.mask_odd()
    data.plot()
    #bc.df.to_csv('/Users/rhf/tmp/df.csv')

def biosans_sensitivity():
    from sans.hfir.biosans.data import Data
    bc = Data("/HFIR/CG3/IPTS-0000/exp327/Datafiles/BioSANS_exp327_scan0039_0001.xml")
    # bc = Data("/Users/rhf/Dropbox (ORNL)/DocumentsWorkstation/SANS/BioSans/20160621-SensitivityCorrupted/BioSANS_exp318_scan0185_0001.xml")
    bc.place_detectors_in_space()
    # bc.plot()

    data = Data("/HFIR/CG3/IPTS-0000/exp327/Datafiles/BioSANS_exp327_scan0045_0001.xml")
    #data = Data("/Users/rhf/Dropbox (ORNL)/DocumentsWorkstation/SANS/BioSans/20160621-SensitivityCorrupted/BioSANS_exp318_scan0034_0001.xml")
    data.set_beam_center(bc)
    #data.plot()
    data.calculate_q_values()
    #data.plot()
    #print(data.df)
    data.correct_solid_angle()
    #print(data.df)
    #data.plot_iq_errors()
    #data.plot_iq()

    #
    # Clone the wing detector example
    #
#     data_wing = copy.deepcopy(data)
#     data_wing.df = data_wing[data_wing['name'] == "wing".encode("utf-8") ]
#     #data_wing.plot()
#     data_wing.plot_iq()

#     flood = Data("/Users/rhf/Dropbox (ORNL)/DocumentsWorkstation/SANS/BioSans/20160621-SensitivityCorrupted/BioSANS_exp318_scan0034_0001.xml")
#     flood.compute_sensitivity()
#     data.correct_sensitivity(flood)
#     data.plot()

    flood = Data("/SNS/users/m2d/user_reductions/Datafiles/BioSANS_exp327_scan0016_0001.xml")
    # Discar wing detector
    #flood.normalization(monitor=False)
    flood.df = flood[flood['name'] == "main".encode("utf-8") ]
    #flood.plot()
    flood.compute_sensitivity()
    #print(flood.df)
    #flood.plot()

    data.df = data[data['name'] == "main".encode("utf-8") ]
    data.plot()
    data.correct_sensitivity(flood)
    data.plot()
    #print(data.df)

def biosans():
    from sans.hfir.biosans.data import Data
    bc = Data("/HFIR/CG3/IPTS-0000/exp327/Datafiles/BioSANS_exp327_scan0039_0001.xml")
    # bc = Data("/Users/rhf/Dropbox (ORNL)/DocumentsWorkstation/SANS/BioSans/20160621-SensitivityCorrupted/BioSANS_exp318_scan0185_0001.xml")
    bc.place_detectors_in_space()
    # bc.plot()

    data = Data("/HFIR/CG3/IPTS-0000/exp327/Datafiles/BioSANS_exp327_scan0045_0001.xml")
    #data = Data("/Users/rhf/Dropbox (ORNL)/DocumentsWorkstation/SANS/BioSans/20160621-SensitivityCorrupted/BioSANS_exp318_scan0034_0001.xml")
    data.set_beam_center(bc)
    #data.plot()
    data.calculate_q_values()
    #data.plot()
    #print(data.df)
    data.correct_solid_angle()
    #print(data.df)
    data.plot_iq_errors()
    data.plot_iq()


def main():
    #gpsans()
    biosans()
    #biosans_sensitivity()


if __name__ == "__main__":
    main()
