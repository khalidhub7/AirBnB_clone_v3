#!/usr/bin/python3
""" Amenity CRUD """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Retrieve list of all Amenity objects """
    amenities_list = [amenity.to_dict()
                      for amenity in storage.all(Amenity).values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieve Amenity object by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete Amenity object by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Create a new Amenity object """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Update Amenity object by id """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    ignore_list = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_list:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
