#!/usr/bin/python3
'''
    Test file for index api endpoint
'''
import unittest
import sys
import json
from models import storage
from api.v1.app import app
from sys import getdefaultencoding as defenc


class Test_Index(unittest.TestCase):
    '''
        Unittest class for testing index api endpoint
    '''

    def setUp(self):
        '''
            Starts up flask for testing
        '''
        self.test_app = app.test_client()

    def test_app_status(self):
        """
        Tests /status endpoint
        """
        response = self.test_app.get('/api/v1/status')
        self.assertEqual(json.loads(
            response.get_data().decode(defenc())),
            {'status': 'OK'}
        )

    def test_app_stats(self):
        """
        Tests /stats endpoint
        """
        response = self.test_app.get('/api/v1/stats')
        self.assertEqual(json.loads(
            response.get_data().decode(defenc())),
            {
                "amenities": storage.count("Amenity"),
                "cities": storage.count("City"),
                "places": storage.count("Place"),
                "reviews": storage.count("Review"),
                "states": storage.count("State"),
                "users": storage.count("User")
            }
        )
