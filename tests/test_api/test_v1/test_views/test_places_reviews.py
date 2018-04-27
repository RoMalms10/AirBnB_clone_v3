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


class Test_Reviews(unittest.TestCase):
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

    def test_reviews_all_by_place_id(self):
        '''
            Testing function that lists all reviews of a place
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        review1 = classes['Review'](text="Nice place",
                                    place_id=place1.id, user_id=user1.id)
        review1.save()
        count = storage.count("Review")
        response = self.test_app.get(
            '/api/v1/places/{}/reviews'.format(place1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(len(check), count)
        city1.delete()
        state1.delete()
        user1.delete()
        place1.delete()
        review1.delete()

    def test_reviews_all_by_place_id_invalid_id(self):
        '''
            Test all function with invalid ID
        '''
        response = self.test_app.get('/api/v1/places/nopID/reviews')
        self.assertEqual(response.status_code, 404)

    def test_reviews_fetch_by_id(self):
        '''
            Testing function to fetch review by review ID
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        review1 = classes['Review'](text="Nice place",
                                    place_id=place1.id, user_id=user1.id)
        review1.save()
        response = self.test_app.get('/api/v1/reviews/{}'.format(review1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(check['id'], review1.id)
        city1.delete()
        state1.delete()
        user1.delete()
        place1.delete()
        review1.delete()

    def test_reviews_fetch_by_id_invalid_id(self):
        '''
            Testing fetch review by review id with invalid ID
        '''
        response = self.test_app.get('/api/v1/reviews/nopID')
        self.assertEqual(response.status_code, 404)

    def test_reviews_delete_by_review_id(self):
        '''
            Test delete by review id function
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        review1 = classes['Review'](text="Nice place",
                                    place_id=place1.id, user_id=user1.id)
        review1.save()
        response = self.test_app.delete('/api/v1/reviews/{}'.format(review1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(storage.get("Review", review1.id), None)
        city1.delete()
        state1.delete()
        user1.delete()
        place1.delete()

    def test_reviews_delete_invalid_id(self):
        '''
            Test delete function with invalid ID
        '''
        response = self.test_app.delete('/api/v1/reviews/nopID')
        self.assertEqual(response.status_code, 404)

    def test_reviews_create(self):
        '''
            Test review create function
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        data = json.dumps({"text": "Nice place",
                           "place_id": str(place1.id),
                           "user_id": str(user1.id)})
        response = self.test_app.post(
            '/api/v1/places/{}/reviews'.format(place1.id),
            data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        review1 = storage.get("Review", check['id'])
        self.assertTrue(review1)
        self.assertEqual(response.status_code, 201)
        city1.delete()
        state1.delete()
        user1.delete()
        place1.delete()
        review1.delete()

    def test_reviews_create_invalid_places_id(self):
        '''
            Test review create function with invalid state ID
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        data = json.dumps({"text": "Nice place",
                           "place_id": str(place1.id),
                           "user_id": str(user1.id)})
        response = self.test_app.post(
            '/api/v1/places/nopID/reviews',
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        state1.delete()
        city1.delete()
        user1.delete()
        place1.delete()

    def test_reviews_create_invalid_JSON(self):
        '''
            Test review create with invalid JSON
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        data = '{}'
        response = self.test_app.post(
            '/api/v1/places/{}/reviews'.format(state1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        state1.delete()
        city1.delete()
        user1.delete()
        place1.delete()

    def test_reviews_create_no_text_key(self):
        '''
            Test city create without a text key
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        data = json.dumps({"place_id": str(place1.id),
                           "user_id": str(user1.id)})
        response = self.test_app.post(
            '/api/v1/places/{}/reviews'.format(state1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        state1.delete()
        city1.delete()
        user1.delete()
        place1.delete()

    def test_reviews_create_no_user_id_key(self):
        '''
            Test city create without a user_id key
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        data = json.dumps({"text": "Cool place",
                           "place_id": str(place1.id)})
        response = self.test_app.post(
            '/api/v1/places/{}/reviews'.format(state1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        state1.delete()
        city1.delete()
        user1.delete()
        place1.delete()

    def test_reviews_create_wrong_user_id_key(self):
        '''
            Test review create with wrong a user_id key
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        data = json.dumps({"text": "Cool place",
                           "place_id": str(place1.id),
                           "user_id": "1"})
        response = self.test_app.post(
            '/api/v1/places/{}/reviews'.format(state1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        state1.delete()
        city1.delete()
        user1.delete()
        place1.delete()

    def test_reviews_create_wrong_place_id_key(self):
        '''
            Test review create with wrong a place_id key
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        data = json.dumps({"text": "Cool place",
                           "place_id": "50",
                           "user_id": str(user1.id)})
        response = self.test_app.post(
            '/api/v1/places/{}/reviews'.format(state1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        state1.delete()
        city1.delete()
        user1.delete()
        place1.delete()

    def test_reviews_update(self):
        '''
            Test review update function
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        review1 = classes['Review'](text="Nice place",
                                    place_id=place1.id, user_id=user1.id)
        review1.save()
        data = json.dumps({"text": "Bad place"})
        response = self.test_app.put(
            'api/v1/reviews/{}'.format(review1.id),
            data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(check['text'], 'Bad place')
        state1.delete()
        city1.delete()
        user1.delete()
        place1.delete()
        review1.delete()

    def test_reviews_update_invalid_id(self):
        '''
            Test city update function with invalid city id
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        review1 = classes['Review'](text="Nice place",
                                    place_id=place1.id, user_id=user1.id)
        review1.save()
        data = json.dumps({"text": "Bad place"})
        response = self.test_app.put(
            '/api/v1/reviews/nopID',
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        state1.delete()
        city1.delete()
        user1.delete()
        place1.delete()
        review1.delete()

    def test_reviews_update_invalid_JSON(self):
        '''
            Test city update function with invalid JSON
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        review1 = classes['Review'](text="Nice place",
                                    place_id=place1.id, user_id=user1.id)
        review1.save()
        data = '{}'
        response = self.test_app.put(
            '/api/v1/reviews/{}'.format(review1.id),
            data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        state1.delete()
        city1.delete()
        user1.delete()
        place1.delete()
        review1.delete()

    def test_reviews_ignore_keys(self):
        '''
            Test to see if id, updated_at, and created_at keys are skipped
        '''
        state1 = classes['State'](name="California")
        state1.save()
        city1 = classes['City'](name="San Francisco", state_id=state1.id)
        city1.save()
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        place1 = classes['Place'](name="Blue Shoe",
                                  city_id=city1.id, user_id=user1.id)
        place1.save()
        review1 = classes['Review'](text="Nice place",
                                    place_id=place1.id, user_id=user1.id)
        review1.save()
        data = '{"created_at": "nop",\
                 "updated_at": "nop", "id": "nop", "user_id": "nop",\
                 "place_id": "nop"}'
        response = self.test_app.put(
            'api/v1/reviews/{}'.format(review1.id),
            data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertNotEqual(review1.id, "nop")
        self.assertNotEqual(review1.updated_at, "nop")
        self.assertNotEqual(review1.created_at, "nop")
        self.assertNotEqual(review1.user_id, "nop")
        self.assertNotEqual(review1.place_id, "nop")
        state1.delete()
        city1.delete()
        user1.delete()
        place1.delete()
        review1.delete()
