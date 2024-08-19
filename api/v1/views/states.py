#!/usr/bin/python3
""" State CRUD """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Return list of all State objects """
    states_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieve State object by id """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Delete State object by id """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Create a new State object """
    data = request.get_json(silent=True)

    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Update State object by id """
    data = request.get_json(silent=True)

    if not data:
        abort(400, description="Not a JSON")

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    ignore_list = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_list:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
