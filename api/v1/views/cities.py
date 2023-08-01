#!/usr/bin/python3
"""Module to handle the data in data in state table
"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State


@app_views.route('/state/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Returns the list of states"""
    myList = []
    states = storage.get(State, state_id)
    if not state:
        abort(404)

    for unit_class in state.cities:
        myList.append(unit_class.to_dict())

    return jsonify(myList)


@app_views.route('/city/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """Get a specific city with a given city_id
    """
    city_class = storage.all(City).values()
    for unit_class in city_class:
        if unit_class.id == city_id:
            return jsonify(unit_class)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city and saves"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Uses POST to create and update the state data"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    city = City(**data)
    city.state_id = state.id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Updates data in city that aligns with a given city_id
    using the PUT method"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    request_data = request.get_json()

    for key, value in request_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict), 200)
