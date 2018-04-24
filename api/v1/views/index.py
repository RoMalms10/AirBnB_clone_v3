#!/usr/bin/python3
'''
    Module containing instructins for the flask blueprint app_views
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage, classes

@app_views.route('/status')
def status():
    '''
    Returns a STATUS OK when pinged
    '''
    return jsonify({'status': 'OK'})

@app_views.route('/stats')
def count_objects():
    '''
    Returns the jsonified version of each counted object
    '''
    count_dict = {}
    for key, value in classes.items():
        if key != "BaseModel":
            count_dict[key.lower()] = storage.count(key)
    return jsonify(count_dict)