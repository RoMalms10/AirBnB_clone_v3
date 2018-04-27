#!/usr/bin/python3
'''
    Test file for cities api endpoint
'''
import unittest
import sys
import json
from models import storage, classes
from api.v1.app import app
from sys import getdefaultencoding as defenc


class Test_Cities(unittest.TestCase):
    '''
        Unittest class for testing cities api endpoint
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

    def test_cities_all_by_state_id(self):
        '''
            Testing function that lists all cities of a state
        '''
        state1 = classes['State'](name="California")
        state1.save()
        state2 = classes['State'](name="New York")
        state2.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        city2 = classes['City'](name="Los Angeles", state_id=state1.id)
        city2.save()
        city3 = classes['City'](name="New York", state_id=state2.id)
        city3.save()
        count = len(state1.cities)
        response = self.test_app.get(
            '/api/v1/states/{}/cities'.format(state1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(len(check), count)
        city1.delete()
        city2.delete()
        city3.delete()
        state1.delete()
        state2.delete()

    def test_cities_all_by_state_id_invalid_id(self):
        '''
            Test all function with invalid ID
        '''
        response = self.test_app.get('/api/v1/states/nopID/cities')
        self.assertEqual(response.status_code, 404)

    def test_cities_fetch_by_id(self):
        '''
            Testing function to fetch city by city ID
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        response = self.test_app.get('/api/v1/cities/{}'.format(city1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(check['id'], city1.id)
        city1.delete()
        state1.delete()

    def test_cities_fetch_by_id_invalid_id(self):
        '''
            Testing fetch city by city id with invalid ID
        '''
        response = self.test_app.get('/api/v1/cities/nopID')
        self.assertEqual(response.status_code, 404)

    def test_cities_delete_by_city_id(self):
        '''
            Test delete by city id function
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        response = self.test_app.delete('/api/v1/cities/{}'.format(city1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(storage.get("City", city1.id), None)
        state1.delete()

    def test_cities_delete_invalid_id(self):
        '''
            Test delete function with invalid ID
        '''
        response = self.test_app.delete('/api/v1/cities/nopID')
        self.assertEqual(response.status_code, 404)

    def test_cities_create(self):
        '''
            Test city create function
        '''
        state1 = classes['State'](name="California")
        state1.save()
        data = json.dumps({"name": "San Francisco"})
        response = self.test_app.post(
            '/api/v1/states/{}/cities'.format(state1.id),
            data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        city1 = storage.get("City", check['id'])
        self.assertTrue(city1)
        self.assertEqual(response.status_code, 201)
        city1.delete()
        state1.delete()

    def test_cities_create_invalid_state_id(self):
        '''
            Test city create function with invalid state ID
        '''
        data = json.dumps({"name": "San Francisco"})
        response = self.test_app.post(
            '/api/v1/states/nopID/cities',
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_cities_create_invalid_JSON(self):
        '''
            Test city create with invalid JSON
        '''
        state1 = classes['State'](name="California")
        state1.save()
        data = '{}'
        response = self.test_app.post(
            '/api/v1/states/{}/cities'.format(state1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        state1.delete()

    def test_cities_create_no_name_key(self):
        '''
            Test city create without a name key
        '''
        state1 = classes['State'](name="California")
        state1.save()
        data = '{"nop": "nop"}'
        response = self.test_app.post(
            '/api/v1/states/{}/cities'.format(state1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        state1.delete()

    def test_cities_update(self):
        '''
            Test city update function
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        data = json.dumps({"name": "Mendocino"})
        response = self.test_app.put(
            'api/v1/cities/{}'.format(city1.id),
            data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(check['name'], 'Mendocino')
        city1.delete()
        state1.delete()

    def test_cities_update_invalid_id(self):
        '''
            Test city update function with invalid city id
        '''
        data = json.dumps({"name": "Mendocino"})
        response = self.test_app.put(
            '/api/v1/cities/nopID',
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_cities_update_invalid_JSON(self):
        '''
            Test city update function with invalid JSON
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        data = '{}'
        response = self.test_app.put(
            '/api/v1/cities/{}'.format(city1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        city1.delete()
        state1.delete()

    def test_cities_ignore_keys(self):
        '''
            Test to see if id, updated_at, and created_at keys are skipped
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        data = '{"created_at": "nop",\
                 "updated_at": "nop", "id": "nop", "state_id": "nop"}'
        response = self.test_app.put(
            'api/v1/cities/{}'.format(city1.id),
            data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertNotEqual(city1.id, "nop")
        self.assertNotEqual(city1.updated_at, "nop")
        self.assertNotEqual(city1.created_at, "nop")
        self.assertNotEqual(city1.state_id, "nop")
        city1.delete()
        state1.delete()
