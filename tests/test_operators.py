'''
Created on Sep 7, 2016

@author: rhf
'''
import unittest



class Test(unittest.TestCase):


    def test_gpsans(self):
        from sans.hfir.gpsans.data import Data
        d1 = Data("/HFIR/CG2/IPTS-17367/exp137/Datafiles/CG2_exp137_scan0067_0001.xml")
        d2 = Data("/HFIR/CG2/IPTS-17367/exp137/Datafiles/CG2_exp137_scan0067_0001.xml")
        d1+=d2
        self.assertEqual((d2.df.counts + d2.df.counts).sum().nominal_value, d1.df.counts.sum().nominal_value)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()