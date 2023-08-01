#!/usr/bin/python3
"""Module to handle the data in data in state table
"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State


@app_views.route('/state', methods=['GET'],
                 strict_slashes=False)
def get_state():
    """Returns th list of states"""
    myList = []
    states_class = storage.all(State).values()
    for unit_class in states_class:
        myList.append(unit_class.to_dict())

    return jsonify(myList)


@app_views.route('/state/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_id(state_id):
    """Get a specific state with a given state_id
    """
    states_class = storage.all(State).values()
    for unit_class in states_class:
        if unit_class.id == state_id:
            return jsonify(unit_class)
    abort(404)


@app_views.route('/state/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state and saves"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/state', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """Uses POST to create and update the state data"""

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/state/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Updates data in state that aligns with a given state_id
    using the PUT method"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    request_data = request.get_json()

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict), 200)
