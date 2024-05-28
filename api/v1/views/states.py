#!/usr/bin/python3
""" States_RestFul API actions """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ return list of all_states """
    list_objs = []
    for i in storage.all('State').values():
        list_objs.append(i.to_dict())
    return jsonify(list_objs)


@app_views.route('/api/v1/states/<state_id>', methods=['GET'])
def get_one_obj(state_id):
    """ return 1 obj by id """
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_obj(state_id):
    """ delete state obj """
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states', methods=['POST'])
def create_obj():
    """ create state obj """
    new = {}
    if request.is_json():
        for i, j in request.get_json().items():
            new[i] = j
        if 'name' not in new:
            abort(400, description="Missing name")
        new_obj = State(**new)
        new_obj.save
        return jsonify(new_obj.to_dict()), 201
    abort(400, description="Not a JSON")


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_obj(state_id):
    """ update state obj """
    if request.is_json():
        obj = storage.get('State', state_id)
        if obj is None:
            abort(404)
        ignore_list = ['id', 'created_at', 'updated_at']
        for i, j in request.get_json().items():
            if i not in ignore_list:
                setattr(obj, i, j)
        obj.save()
        return jsonify(obj.to_dict()), 200
    abort(400, description="Not a JSON")
