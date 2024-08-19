#!/usr/bin/python3
""" Places objects that handle all default RESTful API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Retrieve list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieve a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Delete a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Create a new Place object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")

    place = Place(city_id=city_id, **data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update a Place object by id """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    ignore_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_list:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """ Retrieve all Place objects depending on the JSON in the body of the request """
    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")

    obj = request.get_json()
    if not obj:
        return jsonify([place.to_dict() for place in storage.all(Place).values()])

    places = []
    amenities = []

    # Get all cities from states if states passed
    states = obj.get('states', [])
    cities = obj.get('cities', [])
    amenities = obj.get('amenities', [])

    city_ids = set()
    for state_id in states:
        state = storage.get('State', state_id)
        if state:
            city_ids.update(city.id for city in state.cities)

    city_ids.update(cities)

    for place in storage.all(Place).values():
        if place.city_id in city_ids:
            if not amenities:
                places.append(place.id)
            else:
                if all(amenity.id in amenities for amenity in place.amenities):
                    places.append(place.id)

    return jsonify([storage.get(Place, place_id).to_dict() for place_id in places])
