#!/usr/bin/python3
'''
    Module containing instructions for the flask blueprint app_views with
    Place objects
'''
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, classes


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_all_places_by_city_id(city_id):
    '''
    Retrieves all Places objects associated with city_id
    Returns:
        404 error if city_id doesn't match a City object
        List of places associated with City object on success
    '''
    cls_obj = storage.get("City", city_id)
    if cls_obj is None:
        abort(404)
    else:
        obj_list = cls_obj.places
        cls_list = []
        for obj in obj_list:
            cls_list.append(obj.to_dict())
        return jsonify(cls_list)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def post_make_new_place(city_id):
    '''
    When a POST request is made, a Places object is created with the values
    in the request associated with the city_id
    Returns:
        Raises 404 if city_id not associated with a City object or user_id not
            associated with a User object
        Raises a 400 error if no valid JSON or if there is no name or if there
            is no user_id
        The new Places object with code 201
    '''
    post_dict = request.get_json()
    cls_obj = storage.get("City", city_id)
    if cls_obj is None:
        abort(404)
    if not post_dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in post_dict:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    usr_obj = storage.get("User", post_dict["user_id"])
    if usr_obj is None:
        abort(404)
    if "name" not in post_dict:
        return make_response(jsonify({"error": "Missing name"}), 400)
    post_dict["city_id"] = city_id
    new_place = classes["Place"](**post_dict)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_specific_place(place_id):
    '''
    When a GET request is made with an extra parameter, this method will
    look for the Place ID specified and return the JSON format of that
    object.
    Otherwise, raises a 404
    '''
    cls_obj = storage.get("Place", place_id)
    if cls_obj is None:
        abort(404)
    else:
        return jsonify(cls_obj.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_specific_place(place_id):
    '''
    When a DELETE request is made with the <place_id> parameter, this method
    will look for the Place object that matches and remove it from the database
    Otherwise, raises a 404
    '''
    cls_obj = storage.get("Place", place_id)
    if cls_obj is None:
        abort(404)
    else:
        storage.delete(cls_obj)
        return jsonify({}), 200


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_specific_place(place_id):
    '''
    When a PUT request is made, the object that corresponds to the correct
    Place ID is updated with the information passed in the request
    Return:
        If no object with ID matches, raise a 404 code
        The Place object with a status code 200
    '''
    cls_obj = storage.get("Place", place_id)
    if cls_obj is None:
        abort(404)
    else:
        put_dict = request.get_json()
        if not put_dict:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        put_dict.pop("id", None)
        put_dict.pop("created_at", None)
        put_dict.pop("updated_at", None)
        put_dict.pop("city_id", None)
        for key, value in put_dict.items():
            setattr(cls_obj, key, value)
        cls_obj.save()
        return jsonify(cls_obj.to_dict()), 200
