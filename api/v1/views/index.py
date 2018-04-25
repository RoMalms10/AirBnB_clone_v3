#!/usr/bin/python3
'''
    Module containing instructions for the flask blueprint app_views
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage, classes


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    '''
    Returns a STATUS OK when pinged
    '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def count_objects():
    '''
    Returns the jsonified version of each counted object
    '''
    return jsonify({
        "amenities": storage.count(classes["Amenity"]),
        "citites": storage.count(classes["City"]),
        "places": storage.count(classes["Place"]),
        "reviews": storage.count(classes["Review"]),
        "states": storage.count(classes["State"]),
        "users": storage.count(classes["User"])
    })
