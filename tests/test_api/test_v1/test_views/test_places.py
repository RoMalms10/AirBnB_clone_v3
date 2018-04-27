#!/usr/bin/python3
'''
    Test file for places api endpoint
'''
import unittest
import sys
import json
from models import storage, classes
from api.v1.app import app
from sys import getdefaultencoding as defenc


class Test_places(unittest.TestCase):
    '''
        Unittest class for testing places api endpoint
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

    def test_places_all_by_city(self):
        '''
            Testing function that lists all places in a city
        '''
        user1 = classes['User'](
            name="Billy", email="Nope", password="Nope")
        user1.save()
        state1 = classes['State'](
            name="California")
        state1.save()
        city1 = classes['City'](
            name="San Francisco", state_id=state1.id)
        city1.save()
        city2 = classes['City'](
            name="Los Angeles", state_id=state1.id)
        city2.save()
        place1 = classes['Place'](
            name="Blue Shoe", city_id=city1.id, user_id=user1.id)
        place1.save()
        place2 = classes['Place'](
            name="Little Ranch", city_id=city1.id, user_id=user1.id)
        place2.save()
        place3 = classes['Place'](
            name="Home Sweet Home", city_id=city2.id, user_id=user1.id)
        place3.save()
        count = len(city1.places)
        response = self.test_app.get(
            '/api/v1/cities/{}/places'.format(city1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(len(check), count)
        place1.delete()
        place2.delete()
        place3.delete()
        city1.delete()
        city2.delete()
        state1.delete()
        user1.delete()

    def test_places_all_invalid_id(self):
        '''
            Test all function with invalid city id
        '''
        response = self.test_app.get('/api/v1/cities/nopID/places')
        self.assertEqual(response.status_code, 404)

    def test_places_fetch_by_id(self):
        '''
            Test function to fetch a place by it's id
        '''
        user1 = classes['User'](name="Billy", email="Nope", password="Nope")
        user1.save()
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        place1 = classes['Place'](
            name="Blue Shoe", city_id=city1.id, user_id=user1.id)
        place1.save()
        response = self.test_app.get(
            '/api/v1/places/{}'.format(place1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(place1.id, check['id'])
        place1.delete()
        city1.delete()
        user1.delete()
        state1.delete()

    def test_places_fetch_by_id_invalid_id(self):
        '''
            Test place fetch by id with an invlid ID
        '''
        response = self.test_app.get('/api/v1/places/nopID')
        self.assertEqual(response.status_code, 404)

    def test_places_delete(self):
        '''
            Testing place delete by ID function
        '''
        user1 = classes['User'](name="Billy", email="Nope", password="Nope")
        user1.save()
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        place1 = classes['Place'](
            name="Blue Shoe", city_id=city1.id, user_id=user1.id)
        place1.save()
        response = self.test_app.delete(
            '/api/v1/places/{}'.format(place1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(storage.get("Place", place1.id), None)
        city1.delete()
        user1.delete()
        state1.delete()

    def test_places_delete_invalid_id(self):
        '''
            Test delete with invalid place id
        '''
        response = self.test_app.delete('/api/v1/places/nopID')
        self.assertEqual(response.status_code, 404)

    def test_places_create(self):
        '''
            Test place create function
        '''
        user1 = classes['User'](name="Billy", email="Nope", password="Nope")
        user1.save()
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        data = json.dumps({"name": "Buddy", "user_id": user1.id})
        response = self.test_app.post(
            '/api/v1/cities/{}/places'.format(city1.id),
            data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        place1 = storage.get("Place", check['id'])
        self.assertTrue(place1)
        self.assertEqual(response.status_code, 201)
        place1.delete()
        city1.delete()
        user1.delete()
        state1.delete()

    def test_places_create_invalid_city_id(self):
        '''
            Test place create with invalid city_id
        '''
        data = json.dumps({"name": "Buddy", "user_id": "user1.id"})
        response = self.test_app.post(
            '/api/v1/cities/nopID/places',
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_places_create_invalid_JSON(self):
        '''
            Test place create with invalid JSON
        '''
        user1 = classes['User'](name="Billy", email="Nope", password="Nope")
        user1.save()
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        data = '{}'
        response = self.test_app.post(
            '/api/v1/cities/{}/places'.format(city1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        user1.delete()
        city1.delete()
        state1.delete()

    def test_places_create_missing_user_key(self):
        '''
            Tests place create with missing user_id key
        '''
        user1 = classes['User'](name="Billy", email="Nope", password="Nope")
        user1.save()
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        data = json.dumps({"name": "Buddy"})
        response = self.test_app.post(
            '/api/v1/cities/{}/places'.format(city1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        city1.delete()
        user1.delete()
        state1.delete()

    def test_places_create_invalid_user_id(self):
        '''
            Tests place create wiht invalid user_id
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        data = json.dumps({"name": "Buddy", "user_id": "nop"})
        response = self.test_app.post(
            '/api/v1/cities/{}/places'.format(city1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        city1.delete()
        state1.delete()

    def test_places_create_missing_name_key(self):
        '''
            Tests place create missing name key
        '''
        user1 = classes['User'](name="Billy", email="Nope", password="Nope")
        user1.save()
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        data = json.dumps({"user_id": user1.id})
        response = self.test_app.post(
            '/api/v1/cities/{}/places'.format(city1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        city1.delete()
        user1.delete()
        state1.delete()

    def test_places_update(self):
        '''
            Tests place update function
        '''
        user1 = classes['User'](name="Billy", email="Nope", password="Nope")
        user1.save()
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        place1 = classes['Place'](
            name="Blue Shoe", city_id=city1.id, user_id=user1.id)
        place1.save()
        data = json.dumps({"name": "Long Horn"})
        response = self.test_app.put(
            'api/v1/places/{}'.format(place1.id),
            data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(check['name'], 'Long Horn')
        place1.delete()
        city1.delete()
        user1.delete()
        state1.delete()

    def test_places_update_invalid_id(self):
        '''
            Test place with invalid place ID
        '''
        data = json.dumps({"name": "Long Horn"})
        response = self.test_app.put(
            '/api/v1/places/nopID',
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_places_update_invalid_JSON(self):
        '''
            Test place update with invalid JSON
        '''
        user1 = classes['User'](name="Billy", email="Nope", password="Nope")
        user1.save()
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        place1 = classes['Place'](
            name="Blue Shoe", city_id=city1.id, user_id=user1.id)
        place1.save()
        data = '{}'
        response = self.test_app.put(
            'api/v1/places/{}'.format(place1.id),
            data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(response.status_code, 400)
        place1.delete()
        city1.delete()
        user1.delete()
        state1.delete()

    def test_places_update_ignore_keys(self):
        '''
            Testing if update ignores keys:
            id
            user_id
            city_id
            created_at
            updated_at
        '''
        user1 = classes['User'](name="Billy", email="Nope", password="Nope")
        user1.save()
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        place1 = classes['Place'](
            name="Blue Shoe", city_id=city1.id, user_id=user1.id)
        place1.save()
        data = '{"created_at": "nop",\
                 "updated_at": "nop", "id": "nop", "city_id": "nop"}'
        response = self.test_app.put(
            'api/v1/cities/{}'.format(city1.id),
            data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertNotEqual(place1.id, "nop")
        self.assertNotEqual(place1.updated_at, "nop")
        self.assertNotEqual(place1.created_at, "nop")
        self.assertNotEqual(place1.city_id, "nop")
        place1.delete()
        user1.delete()
        city1.delete()
        state1.delete()
