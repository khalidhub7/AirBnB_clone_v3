#!/usr/bin/python3
""" State CRUD """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states/', methods=['GET'])
def all_state():
    """ List of all State objects """
    states_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def all_state_id(state_id):
    """ Retrieve State object by id """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_id(state_id):
    """ Delete State object by id """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/', methods=['POST'])
def post_state():
    """ Create a new State object """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """ Update State object by id """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if 'name' in data:
        state.name = data['name']
        storage.save()
        return jsonify(state.to_dict()), 200

    return jsonify({"error": "Missing name"}), 400
