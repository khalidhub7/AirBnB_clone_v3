#!/usr/bin/python3
""" City CRUD """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities_by_state(state_id):
    """ Retrieve list of all City objects for a State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities_list = [city.to_dict() for city in storage.all(
        City).values() if city.state_id == state_id]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieve City object by id """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Delete City object by id """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Create a new City object for a State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Update City object by id """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    ignore_list = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_list:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
