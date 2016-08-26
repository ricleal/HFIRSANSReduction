'''
Created on Aug 25, 2016

@author: rhf
'''

from pprint import pprint


def gpsans():
    from sans.hfir.gpsans.data import Data
    d = Data("/HFIR/CG2/IPTS-17367/exp137/Datafiles/CG2_exp137_scan0001_0001.xml", beam_center = [18,122])    
    #d.plot_with_coordinates()
    d.plot()

def biosans():
    from sans.hfir.biosans.data import Data
    bc = Data("/HFIR/CG3/IPTS-0000/exp327/Datafiles/BioSANS_exp327_scan0039_0001.xml")
    beam_center = bc.beam_center()    
    #bc.plot()
    
    data = Data("/HFIR/CG3/IPTS-0000/exp327/Datafiles/BioSANS_exp327_scan0045_0001.xml", beam_center)
    #data.plot()
    
    
def main():
    #gpsans()
    biosans()


if __name__ == "__main__":
    main()