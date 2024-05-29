#!/usr/bin/python3
"""This module defines the /amenities view
"""

from flask import jsonify, abort, request, make_response  # type: ignore
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities',
                 strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amenities(amenity_id=None):
    """retrieves amenities object from storage and
    displays JSON representation to it.
    """
    if (amenity_id is not None):
        obj = storage.get(Amenity, amenity_id)
        if obj is None:
            abort(404)
        else:
            return jsonify(obj.to_dict())
    else:
        amenities_list = []
        for key, value in storage.all(Amenity).items():
            amenities_list.append(value.to_dict())
        return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes amenity object from storage and displays
    an empty dictionary representation.
    """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates a new amenity object and adds it to storage
    with the given key value pairs.
    """
    try:
        obj_dict = request.get_json()
        if obj_dict is None:
            abort(400, "Not a JSON")
    except Exception:
        abort(400, "Not a JSON")
    if 'name' not in obj_dict:
        abort(400, "Missing name")
    new_amenity = Amenity(**obj_dict)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a amenity object with given keys and values
    """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    try:
        obj_dict = request.get_json()
        if obj_dict is None:
            abort(400, "Not a JSON")
    except Exception:
        abort(400, "Not a JSON")
    for key, value in obj_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
