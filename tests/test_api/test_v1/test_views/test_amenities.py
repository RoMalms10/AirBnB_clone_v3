#!/usr/bin/python3
'''
    Test file for amenities api endpoint
'''
import unittest
import sys
import json
from models import storage
from api.v1.app import app
from sys import getdefaultencoding as defenc


class Test_Amenities(unittest.TestCase):
    '''
        Unittest class for testing amenities api endpoint
    '''

    def setUp(self):
        '''
            Starts up flask for testing
        '''
        self.test_app = app.test_client()
