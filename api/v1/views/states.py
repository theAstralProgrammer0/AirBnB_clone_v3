#!/usr/bin/python3
"""This module defines the /state view
"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states(state_id=None):
    """retrieves states object from storage and
    displays JSON representation to it.
    """
    if (state_id is not None):
        obj = storage.get(State, state_id)
        if obj is None:
            abort(404)
        else:
            return jsonify(obj.to_dict())
    else:
        state_list = []
        for key, value in storage.all(State).items():
            state_list.append(value.to_dict())
        return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes state object from storage and displays
    an empty dictionary representation.
    """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a new state object and adds it to storage
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
    new_state = State(**obj_dict)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Updates a state object with given keys and values
    """
    obj = storage.get(State, state_id)
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
