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


class Test_Users(unittest.TestCase):
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

    def test_users_list_all(self):
        '''
            Testing the list all users function
        '''
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        user2 = classes['User'](email="dog@gmail.com", password="bone")
        user2.save()
        user3 = classes['User'](email="cat@gmail.com", password="milk")
        user3.save()
        count = storage.count("User")
        response = self.test_app.get('/api/v1/users')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(len(check), count)
        user1.delete()
        user2.delete()
        user3.delete()

    def test_users_list_specific(self):
        '''
            Testing passing specific ID
        '''
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        response = self.test_app.get('/api/v1/users/{}'.format(user1.id))
        check = json.loads(response.data.decode(defenc()))
        check_user = check['id']
        self.assertEqual(user1.id, check_user)

    def test_users_invalid_id(self):
        '''
            Test invalid ID passed
        '''
        response = self.test_app.get('/api/v1/users/nopID')
        self.assertEqual(response.status_code, 404)

    def test_users_delete(self):
        '''
            Test delete function
        '''
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        response = self.test_app.delete('/api/v1/users/{}'.format(user1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(storage.get("User", user1.id), None)

    def test_users_delete_invalid_ID(self):
        '''
            Test delete with invalid ID
        '''
        response = self.test_app.delete('/api/v1/users/nopID')
        self.assertEqual(response.status_code, 404)

    def test_users_create(self):
        '''
            Test create function
        '''
        data = json.dumps({"email": "penguin@gmail.com",
                           "password": "cool"})
        response = self.test_app.post('/api/v1/users/',
                                      data=data,
                                      content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        user1 = storage.get("User", check['id'])
        self.assertTrue(user1)
        user1.delete()

    def test_users_create_invalid_json(self):
        '''
            Test create function passing bad JSON data
        '''
        data = '{}'
        response = self.test_app.post('/api/v1/users/',
                                      data=data,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_users_create_no_email(self):
        '''
            Test create function without email key
        '''
        data = '{"nop": "nop", "password": "cool"}'
        response = self.test_app.post('/api/v1/users/',
                                      data=data,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_users_create_no_email(self):
        '''
            Test create function without password key
        '''
        data = '{"email": "penguin@gmail.com", "nop": "nop"}'
        response = self.test_app.post('/api/v1/users/',
                                      data=data,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_users_update(self):
        '''
            Test update function
        '''
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        data = json.dumps({"email": "dog@gmail.com",
                           "password": "bone"})
        response = self.test_app.put('api/v1/users/{}'.format(user1.id),
                                     data=data,
                                     content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(check['email'], 'dog@gmail.com')
        user1.delete()

    def test_users_update_invalid_ID(self):
        '''
            Test update with invalid id
        '''
        response = self.test_app.put('/api/v1/users/nopID')
        self.assertEqual(response.status_code, 404)

    def test_users_update_invalid_json(self):
        '''
            Test update with bad JSON data
        '''
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        data = '{}'
        response = self.test_app.put('api/v1/users/{}'.format(user1.id),
                                     data=data,
                                     content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(response.status_code, 400)
        user1.delete()

    def test_users_update_id_created_at_updated_at(self):
        '''
            Test to see if id, updated_at, and created_at keys are skipped
        '''
        user1 = classes['User'](email="penguin@gmail.com", password="cool")
        user1.save()
        data = '{"created_at": "nop", "updated_at": "nop", "id": "nop"}'
        response = self.test_app.put('api/v1/users/{}'.format(user1.id),
                                     data=data,
                                     content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertNotEqual(user1.id, "nop")
        user1.delete()
