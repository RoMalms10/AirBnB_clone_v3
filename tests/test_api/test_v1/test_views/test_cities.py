#!/usr/bin/python3
'''
    Test file for cities api endpoint
'''
import unittest
import sys
import json
from models import storage
from api.v1.app import app


class Test_Cities(unittest.TestCase):
    '''
        Unittest class for testing cities api endpoint
    '''

    def setUp(self):
        '''
            Starts up flask for testing
        '''
        self.test_app = app.test_client()
