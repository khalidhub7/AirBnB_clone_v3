#!/usr/bin/python3
""" cities_RestFul API actions """
from models import storage
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all City from state
    and return all cities in a state
    """
    cities_objs = []
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    for i in state_obj.cities:
        cities_objs.append(i.to_json())
    return jsonify(cities_objs)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_obj(city_id):
    """Retrieves a City object_
    """
    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_json())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_obj(city_id):
    """ delete city obj """
    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_obj(state_id):
    """ create city obj """
    old = request.get_json(silent=True)
    if old is None:
        abort(400, 'Not a JSON')
    if 'name' not in old:
        abort(400, 'Missing name')
    if not storage.get('State', state_id):
        abort(404)
    old['state_id'] = state_id
    new_obj = City(**old)
    new_obj.save()
    resp = jsonify(new_obj.to_json())
    resp.status_code = 201
    return resp


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_obj(city_id):
    """ update city obj """
    old = request.get_json(silent=True)
    if old is None:
        abort(400, 'Not a JSON')
    ignore_list = ['id', 'state_id', 'created_at', 'updated_at']
    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    for i, j in old.items():
        if i not in ignore_list:
            setattr(obj, i, j)
    obj.save()
    return jsonify(obj.to_json()), 200
