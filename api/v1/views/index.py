#!/usr/bin/python3
'''
    Module containing instructins for the flask blueprint app_views
'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    '''
    '''
    return jsonify({'status': 'OK'})
