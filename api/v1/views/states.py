#!/usr/bin/python3
"""  """
from models import base_model #to dict
from api.v1.views import app_views
from flask import request, not_found, jsonify, make_response
from models import state

@app_views.route('/api/v1/states', methods=['GET'])
def get_obj():
    data = {}
    if request.is_json():
        for i, j in request.get_json().items():
            data[i] = j
    list_objs = []
    for x in data:
        list_objs.append(x)
@app_views.route('/api/v1/states/<id>', methods=['GET'])
def changes(id):
    if id not in state.__dict__:
        raise not_found
@app_views.route('/api/v1/states/<id>', methods=['DELETE'])
def changes_1(id):
    if id not in state.__dict__:
        raise not_found
    return make_response(jsonify({}), 200)
@app_views.route('/api/v1/states', methods=['POST'])
def changes_2():
    new = {}
    if request.is_json():
        for i, j in request.get_json().items():
            new[i] = j
        if 'name' not in new:
            raise 400, print('Missing name')
        return new, 201
    raise not_found, print("Not a JSON")
@app_views.route('/api/v1/states/<id>', methods=['PUT'])
def changes_3(id):
    if id not in state.__dict__:
        raise not_found
    new = {}
    if request.is_json():
        for i, j in request.get_json().items():
            new[i] = j
        for x in new:
            if x == 'name':
                return new[x], 200
    raise not_found, print("Not a JSON")
