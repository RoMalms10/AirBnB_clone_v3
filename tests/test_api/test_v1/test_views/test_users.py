#!/usr/bin/python3
'''
    Test file for users api endpoint
'''
import unittest
import sys
import json
from models import storage
from api.v1.app import app
from sys import getdefaultencoding as defenc


class Test_Users(unittest.TestCase):
    '''
        Unittest class for testing users api endpoint
    '''

    def setUp(self):
        '''
            Starts up flask for testing
        '''
        self.test_app = app.test_client()
