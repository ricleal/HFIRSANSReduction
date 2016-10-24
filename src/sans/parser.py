#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.settings import logger

from abc import ABCMeta, abstractmethod
import os, sys
import xml.etree.ElementTree as ET


class Parser(metaclass=ABCMeta):
    
    @abstractmethod
    def getMetadata(self, xpath):
        pass
    
    @abstractmethod
    def getData(self, xpath):
        pass


class XML(Parser):
    '''
    Generic XML Parser.
    Note that getMetadata and getData were not implemented below!
    Thus, this is still an abstract class and must be implemented
    by a subclass
    '''
    def __init__(self, filename):
        if not os.path.exists(filename):
            logger.error("File {} does not exist!".format(filename))
            sys.exit()
        self._root = self._parse(filename)
    
    def _parse(self, filename):
        logger.info("Parsing: %s."%filename)
        tree = ET.parse(filename)
        root = tree.getroot()
        return root
               
class HDF(Parser):
    '''
    Generic HDF (Nexus?) Parser.
    '''
    def __init__(self, filename):
        #TODO!
        pass
    
    def _parse(self, filename):
        #TODO!
        pass
