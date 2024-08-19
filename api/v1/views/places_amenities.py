#!/usr/bin/python3
"""Link between Place and Amenity objects handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv

STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieve list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")

    if STORAGE_TYPE == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:  # FileStorage
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Delete an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, description="Amenity not found")

    if STORAGE_TYPE == 'db':
        if amenity not in place.amenities:
            abort(404, description="Amenity not linked to the Place")
        place.amenities.remove(amenity)
    else:  # FileStorage
        if amenity_id not in place.amenity_ids:
            abort(404, description="Amenity not linked to the Place")
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Link an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, description="Amenity not found")

    if STORAGE_TYPE == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:  # FileStorage
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
