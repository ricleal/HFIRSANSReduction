'''
Created on Aug 25, 2016

@author: rhf
'''

from pprint import pprint


def gpsans():
    from sans.hfir.gpsans.data import Data
    d = Data("/HFIR/CG2/IPTS-17367/exp137/Datafiles/CG2_exp137_scan0001_0001.xml", move_instrument=True)    
    pprint(d.data)
    pprint(d.meta)
    d.plot()

def biosans():
    from sans.hfir.biosans.data import Data
    d = Data("/HFIR/CG3/IPTS-17252/exp321/Shared/SVP/Edited_Datafiles/BioSANS_exp321_scan0050_0001.xml", move_instrument=True)
    d.plot()
    
def main():
    #gpsans()
    biosans()


if __name__ == "__main__":
    main()