#!/usr/bin/python3
""" Place CRUD """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """ Retrieve list of all Place objects in a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places_list = [place.to_dict() for place in storage.all(
        Place).values() if place.city_id == city_id]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieve Place object by id """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete Place object by id """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Create a new Place object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    new_place = Place(**data, city_id=city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update Place object by id """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    ignore_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_list:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
