#!/usr/bin/python3
'''
    Flask application serving pages:
    /api/v1/status
'''
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.errorhandler(404)
def not_found(error):
    '''
        Handles page not found for API
    '''
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.teardown_appcontext
def close_storage(exception):
    '''
        Closes instance of storage being used
    '''
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
