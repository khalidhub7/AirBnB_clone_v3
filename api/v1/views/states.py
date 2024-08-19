#!/usr/bin/python3
""" state CRUD """
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/states/', methods=['GET'])
def all_state():
    """ list of all State objects """
    from models.state import State
    from models import storage
    states_list = []
    for i in storage.all(State).values():
        states_list.append(i.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def all_state_id(state_id):
    """ list State obj by id """
    from models.state import State
    from models import storage
    states_list = []
    for i in storage.all(State).values():
        if i.id == state_id:
            states_list.append(i.to_dict())
        else:
            abort(404)
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_id(state_id):
    """ delete State obj by id
    ex: curl -X DELETE http://127.0.0.1:5000/api/v1/states/dcbba105-2ad1-4f01-b2fb-3674e355f3c3
    """
    from models.state import State
    from models import storage
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/', methods=['POST'])
def post_state():
    """ post State obj by id
    ex: curl -X POST http://127.0.0.1:5000/api/v1/states/ -H "Content-Type: application/json" -d '{"name": "belfaa"}' -vvv
    """
    from models.state import State
    from models import storage
    from flask import request
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """ post State obj by id
    ex: curl -X PUT http://127.0.0.1:5000/api/v1/states/dcbba105-2ad1-4f01-b2fb-3674e355f3c3 -H "Content-Type: application/json" -d '{"name": "belfaa is so cool"}'
    """
    from models.state import State
    from models import storage
    from flask import request
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    state = storage.get(State, state_id)
    if state is not None:
        state.name = data['name']  # Update only the name
        storage.save()
        return jsonify(state.to_dict()), 200
    abort(404)
