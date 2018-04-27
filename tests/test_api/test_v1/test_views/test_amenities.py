#!/usr/bin/python3
'''
    Test file for states api endpoint
'''
import unittest
import sys
import json
from models import storage, classes
from api.v1.app import app
from sys import getdefaultencoding as defenc


class test_amenities(unittest.TestCase):
    '''
        Unittest class for testing states api endpoint
    '''


    def setUp(self):
        '''
            Starts up flask for testing
        '''
        self.test_app = app.test_client()

    def tearDown(self):
        '''
            Calls after every test
        '''
        storage.close()

    def test_amenities_list_all(self):
        '''
            Testing the list all amenities function
        '''
        amenity1 = classes['Amenity'](name="Shower")
        amenity1.save()
        amenity2 = classes['Amenity'](name="Pet Friendly")
        amenity2.save()
        amenity3 = classes['Amenity'](name="No Smoking")
        amenity3.save()
        count = storage.count("Amenity")
        response = self.test_app.get('/api/v1/amenities')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(len(check), count)
        amenity1.delete()
        amenity2.delete()
        amenity3.delete()

    def test_amenities_list_specific(self):
        '''
            Testing passing specific ID
        '''
        amenity1 = classes['Amenity'](name="Shower")
        amenity1.save()
        response = self.test_app.get('/api/v1/amenities/{}'.format(amenity1.id))
        check = json.loads(response.data.decode(defenc()))
        check_amenity = check['id']
        self.assertEqual(amenity1.id, check_amenity)

    def test_amenities_invalid_id(self):
        '''
            Test invalid ID passed
        '''
        response = self.test_app.get('/api/v1/states/nopID')
        self.assertEqual(response.status_code, 404)

    def test_amenities_delete(self):
        '''
            Test delete function
        '''
        amenity1 = classes['Amenity'](name="Patio")
        amenity1.save()
        response = self.test_app.delete('/api/v1/amenities/{}'.format(amenity1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(storage.get("Amenity", amenity1.id), None)

    def test_amenities_delete_invalid_ID(self):
        '''
            Test delete with invalid ID
        '''
        response = self.test_app.delete('/api/v1/amenities/nopID')
        self.assertEqual(response.status_code, 404)

    def test_amenities_create(self):
        '''
            Test create function
        '''
        data = json.dumps({"name": "Patio"})
        response = self.test_app.post('/api/v1/amenities/',
                                       data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        amenity1 = storage.get("Amenity", check['id'])
        self.assertTrue(amenity1)
        amenity1.delete()


    def test_amenities_create_invalid_json(self):
        '''
            Test create function passing bad JSON data
        '''
        data = '{}'
        response = self.test_app.post('/api/v1/amenities/',
                                       data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_amenities_create_no_name(self):
        '''
            Test create function without name key
        '''
        data = '{"nop": "nop"}'
        response = self.test_app.post('/api/v1/amenities/',
                                       data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_amenities_update(self):
        '''
            Test update function
        '''
        amenity1 = classes['Amenity'](name="Shower")
        amenity1.save()
        data = json.dumps({"name": "Penguins"})
        response = self.test_app.put('api/v1/amenities/{}'.format(amenity1.id),
                                      data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(check['name'], 'Penguins')
        amenity1.delete()

    def test_amenities_update_invalid_ID(self):
        '''
            Test update with invalid id
        '''
        response = self.test_app.put('/api/v1/amenities/nopID')
        self.assertEqual(response.status_code, 404)

    def test_amenities_update_invalid_json(self):
        '''
            Test update with bad JSON data
        '''
        amenity1 = classes['Amenity'](name="Shower")
        amenity1.save()
        data = '{}'
        response = self.test_app.put('api/v1/amenities/{}'.format(amenity1.id),
                                      data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(response.status_code, 400)
        amenity1.delete()

    def test_amenities_update_id_created_at_updated_at(self):
        '''
            Test to see if id, updated_at, and created_at keys are skipped
        '''
        amenity1 = classes['Amenity'](name="Shower")
        amenity1.save()
        data = '{"created_at": "nop", "updated_at": "nop", "id": "nop"}'
        response = self.test_app.put('api/v1/amenities/{}'.format(amenity1.id),
                                      data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertNotEqual(amenity1.id, "nop")
        amenity1.delete()
