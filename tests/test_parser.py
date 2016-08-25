#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Aug 24, 2016

@author: rhf
'''

import unittest
from parser.parser import HFIR 

class Test(unittest.TestCase):


    def setUp(self):
        self.data_file = "/HFIR/CG3/IPTS-17252/exp321/Datafiles/BioSANS_exp321_scan0025_0001.xml"
        

    def tearDown(self):
        pass


    def testHFIR(self):
        d = HFIR(self.data_file)
        self.assertEqual(d.getMetadata("Header/Instrument"), "BioSANS")
        data = d.getData("Data/Detector")
        self.assertEqual(data.shape,(256, 192))
#         import matplotlib.pyplot as plt
#         plt.imshow(data)
#         plt.show()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()