#!/usr/bin/python3
""" User CRUD """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ Retrieve list of all User objects """
    users_list = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieve User object by id """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Delete User object by id """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a new User object """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")

    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Update User object by id """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    ignore_list = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_list:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
