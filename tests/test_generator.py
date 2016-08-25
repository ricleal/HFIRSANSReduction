#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Aug 24, 2016

@author: rhf
'''

import unittest
import pandas as pd
import os
import numpy as np

from instrument import generator

class Test(unittest.TestCase):


    def setUp(self):
        LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))
        self.data_file = os.path.join(LOCAL_DIR, "../src/instrument/biosans.hdf")
        

    def tearDown(self):
        pass


    def testBioSANS(self):
        df = pd.read_hdf(self.data_file, 'BioSANS')
        print("Data frame headers:{}".format(df.columns.values))
        self.assertTrue( np.all( df.columns.values == generator.columns ))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()