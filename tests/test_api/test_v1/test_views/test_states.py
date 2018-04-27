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


class Test_States(unittest.TestCase):
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

    def test_states_list_all(self):
        '''
            Testing the list all states function
        '''
        state1 = classes['State'](name="California")
        state1.save()
        state2 = classes['State'](name="Louisiana")
        state2.save()
        state3 = classes['State'](name="New York")
        state3.save()
        count = storage.count("State")
        response = self.test_app.get('/api/v1/states')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(len(check), count)
        state1.delete()
        state2.delete()
        state3.delete()

    def test_states_list_specific(self):
        '''
            Testing passing specific ID
        '''
        state1 = classes['State'](name="California")
        state1.save()
        response = self.test_app.get('/api/v1/states/{}'.format(state1.id))
        check = json.loads(response.data.decode(defenc()))
        check_state = check['id']
        self.assertEqual(state1.id, check_state)

    def test_states_invalid_id(self):
        '''
            Test invalid ID passed
        '''
        response = self.test_app.get('/api/v1/states/nopID')
        self.assertEqual(response.status_code, 404)

    def test_states_delete(self):
        '''
            Test delete function
        '''
        state1 = classes['State'](name="California")
        state1.save()
        response = self.test_app.delete('/api/v1/states/{}'.format(state1.id))
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(storage.get("State", state1.id), None)

    def test_delete_invalid_ID(self):
        '''
            Test delete with invalid ID
        '''
        response = self.test_app.delete('/api/v1/states/nopID')
        self.assertEqual(response.status_code, 404)

    def test_states_create(self):
        '''
            Test create function
        '''
        data = json.dumps({"name": "California"})
        response = self.test_app.post('/api/v1/states/',
                                       data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        state1 = storage.get("State", check['id'])
        self.assertTrue(state1)
        state1.delete()


    def test_states_create_invalid_json(self):
        '''
            Test create function passing bad JSON data
        '''
        data = '{}'
        response = self.test_app.post('/api/v1/states/',
                                       data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_states_create_no_name(self):
        '''
            Test create function without name key
        '''
        data = '{"nop": "nop"}'
        response = self.test_app.post('/api/v1/states/',
                                       data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_states_update(self):
        '''
            Test update function
        '''
        state1 = classes['State'](name="California")
        state1.save()
        data = json.dumps({"name": "New York"})
        response = self.test_app.put('api/v1/states/{}'.format(state1.id),
                                      data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(check['name'], 'New York')
        state1.delete()

    def test_states_update_invalid_ID(self):
        '''
            Test update with invalid id
        '''
        response = self.test_app.put('/api/v1/states/nopID')
        self.assertEqual(response.status_code, 404)

    def test_states_update_invalid_json(self):
        '''
            Test update with bad JSON data
        '''
        state1 = classes['State'](name="California")
        state1.save()
        data = '{}'
        response = self.test_app.put('api/v1/states/{}'.format(state1.id),
                                      data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertEqual(response.status_code, 400)
        state1.delete()

    def test_states_update_id_created_at_updated_at(self):
        '''
            Test to see if id, updated_at, and created_at keys are skipped
        '''
        state1 = classes['State'](name="California")
        state1.save()
        data = '{"created_at": "nop", "updated_at": "nop", "id": "nop"}'
        response = self.test_app.put('api/v1/states/{}'.format(state1.id),
                                      data=data, content_type='application/json')
        check = json.loads(response.data.decode(defenc()))
        self.assertNotEqual(state1.id, "nop")
        state1.delete()
