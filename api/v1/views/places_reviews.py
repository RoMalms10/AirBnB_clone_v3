#!/usr/bin/python3
'''
    Module containing instructions for the flask blueprint app_views
'''
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, classes


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_all_reviews_by_place_id(place_id):
    '''
    Retrieves all review objects associated with place_id
    Returns:
        404 error if place_id doesn't match a Place object
        List of reviews associated with Place object on success
    '''
    cls_obj = storage.get("Place", place_id)
    if cls_obj is None:
        abort(404)
    else:
        obj_list = cls_obj.reviews
        cls_list = []
        for obj in obj_list:
            cls_list.append(obj.to_dict())
        return jsonify(cls_list)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def post_make_new_review(place_id):
    '''
    When a POST request is made, a review object is created with the values
    in the request associated with the place_id
    Returns:
        Raises 400 error if not valid JSON
        Raises 400 if no text key present
        Raises 404 if place_id not associated with valid Place object
        Raises 400 if no user_id key present
        Raises 404 if user_id isn't associated with a User object
        The new review with code 201
    '''
    post_dict = request.get_json()
    if not post_dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in post_dict:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if storage.get("User", post_dict["user_id"]) is None:
        abort(404)
    if "text" not in post_dict:
        return make_response(jsonify({"error": "Missing text"}), 400)
    cls_obj = storage.get("Place", place_id)
    if cls_obj is None:
        abort(404)
    post_dict["place_id"] = place_id
    new_review = classes["Review"](**post_dict)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def get_specific_review(review_id):
    '''
    When a GET request is made with an extra parameter, this method will
    look for the Review ID specified and return the JSON format of that
    object.
    Otherwise, raises a 404
    '''
    cls_obj = storage.get("Review", review_id)
    if cls_obj is None:
        abort(404)
    else:
        return jsonify(cls_obj.to_dict())


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_spcific_review(review_id):
    '''
    When a DELETE request is made with the <review_id> parameter, this method
    will look for the review object that matches and remove it from the
    database
    Otherwise, raises a 404
    '''
    cls_obj = storage.get("Review", review_id)
    if cls_obj is None:
        abort(404)
    else:
        storage.delete(cls_obj)
        return jsonify({}), 200


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def put_specific_review(review_id):
    '''
    When a PUT request is made, the object that corresponds to the correct
    Review ID is updated with the information passed in the request
    Return:
        If no object with ID matches, raise a 404 code
        The Review object with a status code 200
        Skips following keys:
            id
            created_at
            updated_at
            places_id
            user_id
    '''
    cls_obj = storage.get("Review", review_id)
    if cls_obj is None:
        abort(404)
    else:
        put_dict = request.get_json()
        if not put_dict:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        put_dict.pop("id", None)
        put_dict.pop("created_at", None)
        put_dict.pop("updated_at", None)
        put_dict.pop("place_id", None)
        put_dict.pop("user_id", None)
        for key, value in put_dict.items():
            setattr(cls_obj, key, value)
        cls_obj.save()
        return jsonify(cls_obj.to_dict()), 200
